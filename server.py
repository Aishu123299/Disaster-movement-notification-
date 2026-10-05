from __future__ import annotations

import base64
import smtplib
import json
import mimetypes
import os
import re
import ssl
import threading
import time
from datetime import datetime, timedelta
from email.message import EmailMessage
from email.utils import make_msgid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, unquote, urlencode, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
MAX_REQUEST_BYTES = 65536
RATE_LIMIT_SECONDS = 30
HEAVY_RAIN_THRESHOLD_MM_24H = 64.5
MAX_MONITOR_LOCATIONS = 150
MONITOR_WEATHER_BATCH_SIZE = 20
_last_sent: dict[tuple[str, str], float] = {}
_last_sent_lock = threading.Lock()
_monitor_events: dict[tuple[str, str, str], str] = {}
_monitor_events_lock = threading.Lock()


def load_local_env() -> None:
    env_file = ROOT / ".env"
    if not env_file.is_file():
        return
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def channel_is_configured(channel: str) -> bool:
    if channel == "Email":
        host = os.environ.get("SMTP_HOST", "smtp.gmail.com").strip()
        username = os.environ.get("SMTP_USERNAME", "").strip()
        password = os.environ.get("SMTP_PASSWORD", "").strip()
        sender = os.environ.get("SMTP_FROM", "").strip() or username
        try:
            port = int(os.environ.get("SMTP_PORT", "587"))
        except ValueError:
            return False
        return bool(host and username and password and normalize_email(username) and normalize_email(sender) and 1 <= port <= 65535)

    account_sid = os.environ.get("TWILIO_ACCOUNT_SID", "").strip()
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN", "").strip()
    sender_key = "TWILIO_SMS_FROM" if channel == "SMS" else "TWILIO_WHATSAPP_FROM"
    sender = os.environ.get(sender_key, "").strip()
    credentials_ready = bool(re.fullmatch(r"AC[a-fA-F0-9]{32}", account_sid) and auth_token and not auth_token.lower().startswith("replace_with"))
    sender_ready = bool(sender and not sender.lower().startswith("replace_with"))
    if channel == "WhatsApp":
        content_sid = os.environ.get("TWILIO_WHATSAPP_CONTENT_SID", "").strip()
        sender_ready = sender_ready and bool(re.fullmatch(r"HX[a-fA-F0-9]{32}", content_sid))
    return credentials_ready and sender_ready


def live_whatsapp_is_configured() -> bool:
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID", "").strip()
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN", "").strip()
    sender = os.environ.get("TWILIO_WHATSAPP_FROM", "").strip()
    return bool(
        re.fullmatch(r"AC[a-fA-F0-9]{32}", account_sid)
        and auth_token
        and not auth_token.lower().startswith("replace_with")
        and sender
        and not sender.lower().startswith("replace_with")
        and re.fullmatch(
            r"HX[a-fA-F0-9]{32}",
            os.environ.get("TWILIO_WHATSAPP_LIVE_CONTENT_SID", "").strip(),
        )
    )


def channel_configuration_error(channel: str) -> str | None:
    if channel == "Email":
        host = os.environ.get("SMTP_HOST", "smtp.gmail.com").strip()
        username = os.environ.get("SMTP_USERNAME", "").strip()
        password = os.environ.get("SMTP_PASSWORD", "").strip()
        sender = os.environ.get("SMTP_FROM", "").strip() or username
        missing = [
            key for key in ("SMTP_USERNAME", "SMTP_PASSWORD")
            if not os.environ.get(key, "").strip()
            or os.environ.get(key, "").strip().lower().startswith("replace_with")
        ]
        if missing:
            return f"Gmail email delivery is not configured. Add {', '.join(missing)} to the server .env file and restart Rainwatch."
        if not host:
            return "SMTP_HOST must name a mail server (Gmail uses smtp.gmail.com)."
        if not normalize_email(username) or not normalize_email(sender):
            return "SMTP_USERNAME and SMTP_FROM must be valid email addresses."
        try:
            port = int(os.environ.get("SMTP_PORT", "587"))
        except ValueError:
            return "SMTP_PORT must be a number (Gmail uses 587)."
        if not 1 <= port <= 65535:
            return "SMTP_PORT must be between 1 and 65535."
        return None

    required = ["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN"]
    sender_key = "TWILIO_SMS_FROM" if channel == "SMS" else "TWILIO_WHATSAPP_FROM"
    required.append(sender_key)
    if channel == "WhatsApp":
        required.append("TWILIO_WHATSAPP_CONTENT_SID")
    missing = [
        key for key in required
        if not os.environ.get(key, "").strip()
        or os.environ.get(key, "").strip().lower().startswith("replace_with")
    ]
    if missing:
        return f"{channel} is not configured. Add {', '.join(missing)} to the server .env file and restart Rainwatch."
    if not re.fullmatch(r"AC[a-fA-F0-9]{32}", os.environ["TWILIO_ACCOUNT_SID"].strip()):
        return "TWILIO_ACCOUNT_SID must be a valid Twilio Account SID starting with AC."
    if channel == "WhatsApp" and not re.fullmatch(r"HX[a-fA-F0-9]{32}", os.environ["TWILIO_WHATSAPP_CONTENT_SID"].strip()):
        return "TWILIO_WHATSAPP_CONTENT_SID must be an approved WhatsApp Content SID starting with HX."
    return None


def normalize_phone(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    phone = re.sub(r"[\s().-]", "", value)
    if not re.fullmatch(r"\+[1-9]\d{7,14}", phone):
        return None
    return phone


def normalize_email(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    address = value.strip()
    if len(address) > 254 or not re.fullmatch(r"[^@\s<>]+@[^@\s<>]+\.[^@\s<>]+", address):
        return None
    return address


WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Heavy drizzle",
    56: "Freezing drizzle",
    57: "Heavy freezing drizzle",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    66: "Freezing rain",
    67: "Heavy freezing rain",
    71: "Light snow",
    73: "Snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Light rain showers",
    81: "Rain showers",
    82: "Heavy rain showers",
    85: "Snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Heavy thunderstorm with hail",
}


def fetch_current_weather(location: str) -> tuple[str, dict[str, object]]:
    safe_location = re.sub(r"[\r\n\x00-\x1f\x7f]", " ", location).strip()[:120]
    geocoding_query = urlencode({"name": safe_location, "count": 10, "language": "en", "format": "json"})
    geocoding_request = Request(
        f"https://geocoding-api.open-meteo.com/v1/search?{geocoding_query}",
        headers={"User-Agent": "RainwatchLocalDemo/1.0"},
    )
    with urlopen(geocoding_request, timeout=12) as response:
        geocoding = json.loads(response.read().decode("utf-8"))

    places = geocoding.get("results", [])
    indian_places = [place for place in places if place.get("country_code") == "IN"]
    if not indian_places:
        raise ValueError("We could not find that place in India. Try a nearby city or district name.")

    selected_place = next(
        (place for place in indian_places if place.get("name", "").casefold() == safe_location.casefold()),
        indian_places[0],
    )
    place_parts = [selected_place.get("name"), selected_place.get("admin1"), selected_place.get("country")]
    place_name = ", ".join(dict.fromkeys(part for part in place_parts if isinstance(part, str) and part))
    weather_query = urlencode(
        {
            "latitude": selected_place["latitude"],
            "longitude": selected_place["longitude"],
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
            "timezone": "auto",
        }
    )
    with urlopen(f"https://api.open-meteo.com/v1/forecast?{weather_query}", timeout=12) as response:
        weather = json.loads(response.read().decode("utf-8"))

    current = weather.get("current")
    if not isinstance(current, dict):
        raise ValueError("Current weather is not available for that place right now.")
    return place_name, current


def fetch_live_rainfall(latitude: float, longitude: float) -> dict[str, object]:
    results = fetch_live_rainfall_many(
        [{"id": "location", "name": "Selected location", "state": "", "latitude": latitude, "longitude": longitude}]
    )
    return results[0]


def parse_live_rainfall_weather(weather: object) -> dict[str, object]:
    if not isinstance(weather, dict):
        raise ValueError("Live rainfall data is incomplete. Please try again shortly.")
    current = weather.get("current")
    hourly = weather.get("hourly")
    if not isinstance(current, dict) or not isinstance(hourly, dict):
        raise ValueError("Live rainfall data is incomplete. Please try again shortly.")
    try:
        observed_at = str(current["time"])
        current_time = datetime.fromisoformat(observed_at)
        times = hourly["time"]
        precipitation = hourly["precipitation"]
        if not isinstance(times, list) or not isinstance(precipitation, list) or len(times) != len(precipitation):
            raise ValueError
        hourly_samples = [
            (datetime.fromisoformat(time_value), float(value))
            for time_value, value in zip(times, precipitation)
            if isinstance(time_value, str)
            and isinstance(value, (int, float))
            and not isinstance(value, bool)
            and value >= 0
        ]
        valid_values = [
            value
            for sample_time, value in hourly_samples
            if current_time - timedelta(hours=24) < sample_time <= current_time
        ]
        if not valid_values:
            raise ValueError
        rainfall_24h = sum(valid_values)
        forecast_samples = [
            (sample_time, value)
            for sample_time, value in hourly_samples
            if current_time < sample_time <= current_time + timedelta(hours=24)
        ]
        if not forecast_samples:
            raise ValueError
        first_hour_rainfall = forecast_samples[0][1]
        rain_start_sample = next(
            (
                (sample_time, value)
                for sample_time, value in forecast_samples
                if value >= 0.1
            ),
            None,
        )
        rain_onset = next(
            (
                max(1, round((sample_time - current_time).total_seconds() / 3600))
                for sample_time, value in forecast_samples
                if value >= 0.1
            ),
            None,
        )
        threshold_projection = None
        for sample_time, _ in forecast_samples:
            rolling_rainfall = sum(
                value
                for window_time, value in hourly_samples
                if sample_time - timedelta(hours=24) < window_time <= sample_time
            )
            if rolling_rainfall >= HEAVY_RAIN_THRESHOLD_MM_24H:
                threshold_projection = (sample_time, rolling_rainfall)
                break
        peak_time, peak_rainfall = max(forecast_samples, key=lambda sample: sample[1])
        temperature = float(current["temperature_2m"])
        condition = WEATHER_CODES.get(int(current["weather_code"]), "Current conditions")
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("Live rainfall data is incomplete. Please try again shortly.") from error
    return {
        "observed_at": observed_at,
        "rainfall_24h": round(rainfall_24h, 1),
        "precipitation": float(current.get("precipitation", 0)),
        "temperature": temperature,
        "condition": condition,
        "next_hour_rain_mm": round(first_hour_rainfall, 1),
        "rain_start_hours": rain_onset,
        "rain_start_time": rain_start_sample[0].strftime("%H:%M") if rain_start_sample else None,
        "forecast_peak_hourly_mm": round(peak_rainfall, 1),
        "forecast_peak_hours": max(1, round((peak_time - current_time).total_seconds() / 3600)),
        "forecast_peak_time": peak_time.strftime("%H:%M"),
        "heavy_rain_threshold_hours": (
            max(1, round((threshold_projection[0] - current_time).total_seconds() / 3600))
            if threshold_projection
            else None
        ),
        "heavy_rain_threshold_time": threshold_projection[0].strftime("%H:%M") if threshold_projection else None,
        "heavy_rain_threshold_rainfall_mm": round(threshold_projection[1], 1) if threshold_projection else None,
        "forecast_24h_mm": round(sum(value for _, value in forecast_samples), 1),
    }


def fetch_live_rainfall_many(locations: list[dict[str, object]]) -> list[dict[str, object]]:
    if not locations or len(locations) > MAX_MONITOR_LOCATIONS:
        raise ValueError(f"Monitor between 1 and {MAX_MONITOR_LOCATIONS} Indian cities or districts.")
    for location in locations:
        latitude = location["latitude"]
        longitude = location["longitude"]
        if (
            isinstance(latitude, bool)
            or not isinstance(latitude, (int, float))
            or not 6.0 <= latitude <= 38.6
            or isinstance(longitude, bool)
            or not isinstance(longitude, (int, float))
            or not 68.0 <= longitude <= 98.0
        ):
            raise ValueError("Choose monitoring locations within India.")

    query = urlencode(
        {
            "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m",
            "hourly": "precipitation",
            "past_days": 1,
            "forecast_days": 2,
            "timezone": "auto",
        }
    )
    results: list[dict[str, object]] = []
    for offset in range(0, len(locations), MONITOR_WEATHER_BATCH_SIZE):
        batch = locations[offset:offset + MONITOR_WEATHER_BATCH_SIZE]
        coordinates = urlencode(
            {
                "latitude": ",".join(str(location["latitude"]) for location in batch),
                "longitude": ",".join(str(location["longitude"]) for location in batch),
            }
        )
        request = Request(
            f"https://api.open-meteo.com/v1/forecast?{coordinates}&{query}",
            headers={"User-Agent": "RainwatchLocalDemo/1.0"},
        )
        for attempt in range(2):
            try:
                with urlopen(request, timeout=35) as response:
                    weather_data = json.loads(response.read().decode("utf-8"))
                break
            except HTTPError as error:
                if attempt == 0 and error.code in {500, 502, 503, 504}:
                    time.sleep(2)
                    continue
                raise
            except (TimeoutError, URLError):
                if attempt == 0:
                    time.sleep(2)
                    continue
                raise
        if len(batch) == 1 and isinstance(weather_data, dict):
            weather_items = [weather_data]
        elif isinstance(weather_data, list):
            weather_items = weather_data
        else:
            raise ValueError("Live weather provider returned an invalid multi-location response.")
        if len(weather_items) != len(batch):
            raise ValueError("Live weather provider returned an incomplete location batch.")
        results.extend(parse_live_rainfall_weather(item) for item in weather_items)
    return results


def format_live_rain_alert(
    location: str,
    rainfall_24h: float,
    observed_at: str,
    threshold_hours: int | None = None,
    threshold_time: str | None = None,
    threshold_rainfall: float | None = None,
) -> str:
    safe_location = re.sub(r"[\r\n\x00-\x1f\x7f]", " ", location).strip()[:120]
    safe_time = re.sub(r"[\r\n\x00-\x1f\x7f]", " ", observed_at).strip()[:40]
    if threshold_hours is not None:
        safe_threshold_time = re.sub(r"[\r\n\x00-\x1f\x7f]", " ", threshold_time or "").strip()[:12]
        crossing = (
            f"Forecast projects the rolling 24-hour total may reach at least "
            f"{threshold_rainfall if threshold_rainfall is not None else HEAVY_RAIN_THRESHOLD_MM_24H:g} mm "
            f"in about {threshold_hours} hour(s), around {safe_threshold_time} IST."
        )
    else:
        crossing = f"The rolling 24-hour estimate is at or above {HEAVY_RAIN_THRESHOLD_MM_24H:g} mm."
    return (
        f"RAINWATCH HEAVY RAIN DETECTION · {safe_location}\n"
        f"Open-Meteo estimates {rainfall_24h:g} mm in the current rolling 24-hour window. {crossing}\n"
        f"Model update: {safe_time}.\n"
        "This is a model-based estimate, not an official IMD station observation or warning. "
        "Follow IMD and local authorities for official guidance."
    )


def format_weather_message(place_name: str, current: dict[str, object]) -> str:
    try:
        temperature = float(current["temperature_2m"])
        feels_like = float(current["apparent_temperature"])
        humidity = int(current["relative_humidity_2m"])
        precipitation = float(current["precipitation"])
        wind_speed = float(current["wind_speed_10m"])
        weather_code = int(current["weather_code"])
        observed_at = str(current["time"])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("Current weather data is incomplete. Please try again later.") from error

    condition = WEATHER_CODES.get(weather_code, "Current conditions")
    return (
        f"RAINWATCH WEATHER UPDATE (ONE-TIME)\n{place_name}\n"
        f"Now: {condition}, {temperature:.1f} C (feels like {feels_like:.1f} C).\n"
        f"Humidity: {humidity}%. Rain: {precipitation:g} mm. Wind: {wind_speed:g} km/h.\n"
        f"Observed: {observed_at}.\n"
        "This is a current-conditions snapshot, not an official warning. "
        "Check IMD/local authorities for emergency alerts."
    )


def weather_template_variables(place_name: str, current: dict[str, object]) -> dict[str, str]:
    weather_code = int(current["weather_code"])
    return {
        "1": place_name,
        "2": WEATHER_CODES.get(weather_code, "Current conditions"),
        "3": f"{float(current['temperature_2m']):.1f}",
        "4": f"{float(current['apparent_temperature']):.1f}",
        "5": str(int(current["relative_humidity_2m"])),
        "6": f"{float(current['precipitation']):g}",
        "7": f"{float(current['wind_speed_10m']):g}",
        "8": str(current["time"]).replace("T", " "),
    }


def format_demo_alert_message(location: str, alert_data: dict[str, object]) -> str:
    rainfall = alert_data["rainfall"]
    risk = alert_data["risk"]
    risk_level = alert_data["risk_level"]
    forecast = alert_data["forecast"]
    areas = alert_data["areas"]
    return (
        f"RAINWATCH WEATHER ALERT · {location}\n"
        "DEMO DATA — simulated prediction, not an official warning.\n"
        f"Heavy rainfall detected. Flood risk is {risk} ({risk_level}).\n"
        f"Rainfall: {rainfall} mm. Forecast (next 3 hours): {forecast} mm/hr.\n"
        f"Predicted inundation area: {areas}.\n"
        "Please move to a safe area and follow local authorities for official guidance."
    )


def send_email_alert(recipient: str, location: str, message: str) -> dict[str, str]:
    host = os.environ.get("SMTP_HOST", "smtp.gmail.com").strip()
    port = int(os.environ.get("SMTP_PORT", "587"))
    username = os.environ["SMTP_USERNAME"].strip()
    password = os.environ["SMTP_PASSWORD"].strip().replace(" ", "")
    sender = os.environ.get("SMTP_FROM", "").strip() or username
    safe_location = re.sub(r"[\r\n\x00-\x1f\x7f]", " ", location).strip()[:100]

    email_message = EmailMessage()
    email_message["From"] = sender
    email_message["To"] = recipient
    email_message["Subject"] = f"Rainwatch flood-risk alert — {safe_location}"
    email_message["Message-ID"] = make_msgid()
    email_message.set_content(message)

    with smtplib.SMTP(host, port, timeout=20) as smtp:
        smtp.ehlo()
        smtp.starttls(context=ssl.create_default_context())
        smtp.ehlo()
        smtp.login(username, password)
        refused = smtp.send_message(email_message, from_addr=sender, to_addrs=[recipient])
    if refused:
        details = []
        for _, (code, response) in refused.items():
            detail = response.decode("utf-8", "replace") if isinstance(response, bytes) else str(response)
            detail = re.sub(r"[\r\n\x00-\x1f\x7f]", " ", detail).strip()[:240]
            details.append(f"SMTP {code}: {detail}")
        raise smtplib.SMTPException("; ".join(details))
    return {"sid": email_message["Message-ID"], "status": "accepted"}


def alert_template_variables(location: str, alert_data: dict[str, object]) -> dict[str, str]:
    observed_at = time.strftime("%Y-%m-%d %H:%M IST", time.gmtime(time.time() + 5.5 * 60 * 60))
    return {
        "1": location,
        "2": str(alert_data["rainfall"]),
        "3": str(alert_data["risk"]),
        "4": str(alert_data["risk_level"]),
        "5": str(alert_data["forecast"]),
        "6": str(alert_data["areas"]),
        "7": "Please move to a safe area and follow local authorities for official guidance.",
        "8": observed_at,
    }


def send_twilio_message(
    channel: str,
    phone: str,
    location: str,
    message: str | None = None,
    content_variables: dict[str, str] | None = None,
    content_sid: str | None = None,
) -> dict[str, str]:
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    sender_key = "TWILIO_SMS_FROM" if channel == "SMS" else "TWILIO_WHATSAPP_FROM"
    sender = os.environ[sender_key].strip()

    if channel == "WhatsApp":
        recipient = phone if phone.startswith("whatsapp:") else f"whatsapp:{phone}"
        sender = sender if sender.startswith("whatsapp:") else f"whatsapp:{sender}"
    else:
        recipient = phone

    safe_location = re.sub(r"[\r\n\x00-\x1f\x7f]", " ", location).strip()[:80] or "your area"
    message_fields = {"To": recipient, "From": sender}
    if channel == "WhatsApp" and message is not None:
        message_fields["ContentSid"] = (content_sid or os.environ["TWILIO_WHATSAPP_CONTENT_SID"]).strip()
        message_fields["ContentVariables"] = json.dumps(content_variables or {}, ensure_ascii=True)
    else:
        body = message or (
            f"RAINWATCH TEST MESSAGE\nDelivery check for {safe_location}.\n"
            "This is a test only. No live hazard data was checked. "
            "This is NOT an emergency warning. No action is required."
        )
        message_fields["Body"] = body
    payload = urlencode(message_fields).encode("ascii")
    credentials = base64.b64encode(f"{account_sid}:{auth_token}".encode("utf-8")).decode("ascii")
    request = Request(
        f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json",
        data=payload,
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        method="POST",
    )

    with urlopen(request, timeout=20) as response:
        result = json.loads(response.read().decode("utf-8"))
    sid = result.get("sid")
    if not isinstance(sid, str) or not sid:
        raise ValueError("Twilio accepted no message ID; no delivery can be confirmed.")
    status = str(result.get("status", "accepted"))
    if status.lower() in {"failed", "undelivered", "canceled"}:
        raise ValueError(f"Twilio created the message but reported its status as {status}.")
    return {"sid": sid, "status": status}


class RainwatchHandler(BaseHTTPRequestHandler):
    server_version = "RainwatchLocal/1.0"

    def log_message(self, format_string: str, *args: object) -> None:
        # Keep request logs free of message bodies and phone numbers.
        super().log_message(format_string, *args)

    def send_json(self, status: int, payload: dict[str, object]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        if path == "/api/weather":
            location_values = parse_qs(parsed_path.query, keep_blank_values=True).get("location", ["Pune"])
            location = location_values[0].strip()
            if not location or len(location) > 120:
                self.send_json(400, {"error": "Enter a location under 120 characters."})
                return
            try:
                place_name, current = fetch_current_weather(location)
                self.send_json(
                    200,
                    {
                        "place": place_name,
                        "observed_at": current["time"],
                        "temperature": current["temperature_2m"],
                        "feels_like": current["apparent_temperature"],
                        "humidity": current["relative_humidity_2m"],
                        "precipitation": current["precipitation"],
                        "wind_speed": current["wind_speed_10m"],
                        "condition": WEATHER_CODES.get(int(current["weather_code"]), "Current conditions"),
                    },
                )
            except ValueError as error:
                self.send_json(400, {"error": str(error)})
            except (KeyError, TypeError):
                self.send_json(502, {"error": "Current weather data is incomplete. Please try again shortly."})
            except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError):
                self.send_json(502, {"error": "Could not retrieve current weather right now. Try again shortly."})
            return
        if path == "/api/status":
            self.send_json(
                200,
                {
                    "providers": {"SMS": "Twilio", "WhatsApp": "Twilio", "Email": "Gmail SMTP"},
                    "channels": {
                        "SMS": channel_is_configured("SMS"),
                        "WhatsApp": channel_is_configured("WhatsApp"),
                        "WhatsAppLive": live_whatsapp_is_configured(),
                        "Email": channel_is_configured("Email"),
                    },
                },
            )
            return

        relative_path = unquote(path.lstrip("/")) or "index.html"
        target = (ROOT / relative_path).resolve()
        if target != ROOT and ROOT not in target.parents:
            self.send_json(403, {"error": "Forbidden."})
            return
        if target.name.lower().startswith(".env") and target.name.lower() != ".env.example":
            self.send_json(403, {"error": "Environment files are not available over HTTP."})
            return
        if not target.is_file():
            self.send_json(404, {"error": "Not found."})
            return

        content = target.read_bytes()
        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8" if content_type.startswith("text/") or content_type == "application/javascript" else content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def handle_live_monitor(
        self,
        channel: str,
        recipient: str,
        locations: list[dict[str, object]],
    ) -> None:
        try:
            weather_results = fetch_live_rainfall_many(locations)
        except ValueError as error:
            self.send_json(502, {"error": str(error)})
            return
        except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError) as error:
            detail = re.sub(r"[\r\n\x00-\x1f\x7f]", " ", str(error)).strip()[:300]
            message = f"Live weather provider error: {detail}" if detail else "Could not reach the live weather provider. Try again shortly."
            self.send_json(502, {"error": message})
            return

        results: list[dict[str, object]] = []
        alerts_sent = 0
        for location, live in zip(locations, weather_results):
            name = str(location["name"])
            state = str(location["state"])
            place = f"{name}, {state}"
            rainfall = float(live["rainfall_24h"])
            latitude = float(location["latitude"])
            longitude = float(location["longitude"])
            event_key = (channel, recipient.casefold(), str(location["id"]))
            result: dict[str, object] = {
                "id": location["id"],
                "location": place,
                "rainfall_24h": rainfall,
                "forecast_24h_mm": live["forecast_24h_mm"],
                "next_hour_rain_mm": live["next_hour_rain_mm"],
                "rain_start_hours": live["rain_start_hours"],
                "rain_start_time": live["rain_start_time"],
                "forecast_peak_hourly_mm": live["forecast_peak_hourly_mm"],
                "forecast_peak_hours": live["forecast_peak_hours"],
                "forecast_peak_time": live["forecast_peak_time"],
                "heavy_rain_threshold_hours": live["heavy_rain_threshold_hours"],
                "heavy_rain_threshold_time": live["heavy_rain_threshold_time"],
                "heavy_rain_threshold_rainfall_mm": live["heavy_rain_threshold_rainfall_mm"],
                "observed_at": live["observed_at"],
                "detected": rainfall >= HEAVY_RAIN_THRESHOLD_MM_24H,
                "forecast_heavy_rain": live["heavy_rain_threshold_hours"] is not None,
                "alert_sent": False,
                "already_alerted": False,
            }
            should_alert = result["detected"] or result["forecast_heavy_rain"]
            if not should_alert:
                with _monitor_events_lock:
                    _monitor_events.pop(event_key, None)
                results.append(result)
                continue
            if channel == "WhatsApp" and not live_whatsapp_is_configured():
                result["error"] = (
                    "Live WhatsApp alert is not configured. Add Twilio credentials, sender, "
                    "and approved TWILIO_WHATSAPP_LIVE_CONTENT_SID."
                )
                results.append(result)
                continue
            if channel != "WhatsApp" and not channel_is_configured(channel):
                result["error"] = channel_configuration_error(channel) or f"{channel} is not configured."
                results.append(result)
                continue

            with _monitor_events_lock:
                event = _monitor_events.get(event_key)
                if event in {"sent", "sending"}:
                    result["already_alerted"] = True
                    results.append(result)
                    continue
                _monitor_events[event_key] = "sending"

            threshold_hours = live["heavy_rain_threshold_hours"]
            threshold_time = live["heavy_rain_threshold_time"]
            threshold_rainfall = live["heavy_rain_threshold_rainfall_mm"]
            message = format_live_rain_alert(
                place,
                rainfall,
                str(live["observed_at"]),
                int(threshold_hours) if threshold_hours is not None else None,
                str(threshold_time) if threshold_time is not None else None,
                float(threshold_rainfall) if threshold_rainfall is not None else None,
            )
            template_variables = {
                "1": re.sub(r"[\r\n\x00-\x1f\x7f]", " ", place).strip()[:120],
                "2": f"{rainfall:g}",
                "3": f"{HEAVY_RAIN_THRESHOLD_MM_24H:g}",
                "4": (
                    f"Forecast may reach {float(threshold_rainfall):g} mm in about {threshold_hours} hour(s), around {threshold_time} IST."
                    if threshold_hours is not None
                    else f"The current rolling 24-hour estimate is {rainfall:g} mm."
                ),
            }
            try:
                if channel == "Email":
                    delivery = send_email_alert(recipient, place, message)
                else:
                    delivery = send_twilio_message(
                        channel,
                        recipient,
                        place,
                        message=message,
                        content_variables=template_variables if channel == "WhatsApp" else None,
                        content_sid=(
                            os.environ.get("TWILIO_WHATSAPP_LIVE_CONTENT_SID")
                            if channel == "WhatsApp"
                            else None
                        ),
                    )
            except HTTPError as error:
                with _monitor_events_lock:
                    _monitor_events.pop(event_key, None)
                try:
                    provider_error = json.loads(error.read().decode("utf-8"))
                    detail = str(provider_error.get("message", "")).strip()
                    code = provider_error.get("code")
                    if code:
                        detail = f"{detail} (error {code})".strip()
                except (json.JSONDecodeError, UnicodeDecodeError):
                    detail = ""
                detail = re.sub(r"[\r\n\x00-\x1f\x7f]", " ", detail).strip()[:300]
                result["error"] = f"{channel} rejected the alert: {detail or 'check sender, recipient, and template settings.'}"
            except (TimeoutError, URLError, OSError, smtplib.SMTPException, ValueError) as error:
                with _monitor_events_lock:
                    _monitor_events.pop(event_key, None)
                detail = re.sub(r"[\r\n\x00-\x1f\x7f]", " ", str(error)).strip()[:300]
                result["error"] = f"{channel} alert was not accepted: {detail or 'provider connection failed.'}"
            else:
                with _monitor_events_lock:
                    _monitor_events[event_key] = "sent"
                result["alert_sent"] = True
                result["delivery_status"] = delivery["status"]
                alerts_sent += 1
            results.append(result)

        detected_count = sum(1 for result in results if result["detected"])
        forecast_heavy_rain_count = sum(1 for result in results if result["forecast_heavy_rain"])
        delivery_configured = (
            live_whatsapp_is_configured()
            if channel == "WhatsApp"
            else channel_is_configured(channel)
        )
        delivery_setup_error = None
        if not delivery_configured:
            delivery_setup_error = (
                "Live WhatsApp needs Twilio credentials, a sender, and an approved "
                "TWILIO_WHATSAPP_LIVE_CONTENT_SID."
                if channel == "WhatsApp"
                else channel_configuration_error(channel)
            )
        self.send_json(
            200,
            {
                "ok": True,
                "locations_checked": len(results),
                "detected_count": detected_count,
                "forecast_heavy_rain_count": forecast_heavy_rain_count,
                "alerts_sent": alerts_sent,
                "delivery_configured": delivery_configured,
                "delivery_setup_error": delivery_setup_error,
                "threshold_mm_24h": HEAVY_RAIN_THRESHOLD_MM_24H,
                "results": results,
            },
        )

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path not in {"/api/test-message", "/api/weather-message", "/api/alert", "/api/monitor"}:
            self.send_json(404, {"error": "Not found."})
            return
        is_weather_message = path == "/api/weather-message"
        is_alert = path == "/api/alert"
        is_monitor = path == "/api/monitor"

        if self.headers.get_content_type() != "application/json":
            self.send_json(415, {"error": "Send JSON to the local test endpoint."})
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0
        if content_length < 1 or content_length > MAX_REQUEST_BYTES:
            self.send_json(400, {"error": "Invalid request size."})
            return
        try:
            data = json.loads(self.rfile.read(content_length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.send_json(400, {"error": "Invalid JSON."})
            return
        if not isinstance(data, dict):
            self.send_json(400, {"error": "Invalid request."})
            return

        channel = data.get("channel")
        if is_weather_message:
            requested_channels = data.get("channels")
            if (
                not isinstance(requested_channels, list)
                or not requested_channels
                or len(requested_channels) > 2
                or any(not isinstance(item, str) or item not in {"SMS", "WhatsApp"} for item in requested_channels)
            ):
                self.send_json(400, {"error": "Select SMS, WhatsApp, or both delivery channels."})
                return
            requested_channels = list(dict.fromkeys(requested_channels))
        elif is_monitor:
            if not isinstance(channel, str) or channel not in {"SMS", "WhatsApp", "Email"}:
                self.send_json(400, {"error": "Choose SMS, WhatsApp, or Email for live monitoring alerts."})
                return
            requested_channels = [channel]
        elif isinstance(channel, str) and (
            channel in {"SMS", "WhatsApp"} or is_alert and channel == "Email"
        ):
            requested_channels = [channel]
        else:
            self.send_json(400, {"error": "Choose SMS, WhatsApp, or Email for a Rainwatch alert."})
            return

        if (is_alert or is_monitor) and channel == "Email":
            recipient = normalize_email(data.get("recipient"))
        else:
            recipient_value = data.get("recipient") if is_alert or is_monitor else data.get("phone")
            recipient = normalize_phone(recipient_value)
        location_value = data.get("location", "")
        location = location_value.strip() if isinstance(location_value, str) else ""
        if is_weather_message and data.get("consent") is not True:
            self.send_json(400, {"error": "Confirm that you want one current-weather message before submitting."})
            return
        if is_alert and data.get("consent") is not True:
            self.send_json(400, {"error": "Confirm that you want to send this alert before submitting."})
            return
        if is_monitor and data.get("consent") is not True:
            self.send_json(400, {"error": "Confirm ongoing consent before starting live monitoring."})
            return
        if recipient is None:
            error_message = (
                "Enter a valid email address, for example name@gmail.com."
                if (is_alert or is_monitor) and channel == "Email"
                else "Enter a phone number in international format, for example +919876543210."
            )
            self.send_json(400, {"error": error_message})
            return
        if len(location) > 120 or ((is_weather_message or is_alert) and not location):
            self.send_json(400, {"error": "Enter a location under 120 characters."})
            return
        if is_monitor:
            raw_locations = data.get("locations")
            if (
                not isinstance(raw_locations, list)
                or not raw_locations
                or len(raw_locations) > MAX_MONITOR_LOCATIONS
            ):
                self.send_json(
                    400,
                    {"error": f"Select between 1 and {MAX_MONITOR_LOCATIONS} Indian cities or districts to monitor."},
                )
                return
            locations: list[dict[str, object]] = []
            identifiers: set[str] = set()
            for item in raw_locations:
                if not isinstance(item, dict):
                    self.send_json(400, {"error": "Monitoring locations are invalid."})
                    return
                identifier = item.get("id")
                name = item.get("name")
                state = item.get("state")
                latitude = item.get("latitude")
                longitude = item.get("longitude")
                if (
                    not isinstance(identifier, str)
                    or len(identifier) > 140
                    or not isinstance(name, str)
                    or not name.strip()
                    or len(name) > 80
                    or not isinstance(state, str)
                    or not state.strip()
                    or len(state) > 80
                    or identifier != f"{state}:{name}"
                    or identifier in identifiers
                    or isinstance(latitude, bool)
                    or not isinstance(latitude, (int, float))
                    or isinstance(longitude, bool)
                    or not isinstance(longitude, (int, float))
                ):
                    self.send_json(400, {"error": "Monitoring location details are invalid."})
                    return
                identifiers.add(identifier)
                locations.append(
                    {
                        "id": identifier,
                        "name": re.sub(r"[\r\n\x00-\x1f\x7f]", " ", name).strip(),
                        "state": re.sub(r"[\r\n\x00-\x1f\x7f]", " ", state).strip(),
                        "latitude": latitude,
                        "longitude": longitude,
                    }
                )
            if any(
                not 6.0 <= float(item["latitude"]) <= 38.6
                or not 68.0 <= float(item["longitude"]) <= 98.0
                for item in locations
            ):
                self.send_json(400, {"error": "Choose monitoring locations within India."})
                return
            self.handle_live_monitor(
                channel,
                recipient,
                locations,
            )
            return
        alert_message = None
        alert_variables = None
        if is_alert:
            alert_data = data.get("alert")
            if not isinstance(alert_data, dict):
                self.send_json(400, {"error": "Alert details are missing. Run a prediction and try again."})
                return
            rainfall = alert_data.get("rainfall")
            forecast = alert_data.get("forecast")
            risk = alert_data.get("risk")
            risk_level = alert_data.get("risk_level")
            areas = alert_data.get("areas")
            if (
                isinstance(rainfall, bool)
                or not isinstance(rainfall, (int, float))
                or not 0 <= rainfall <= 1000
                or isinstance(forecast, bool)
                or not isinstance(forecast, list)
                or len(forecast) != 3
                or any(isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 1000 for value in forecast)
                or not isinstance(risk, str)
                or risk not in {"LOW", "MODERATE", "HIGH"}
                or not isinstance(risk_level, str)
                or risk_level not in {"NORMAL", "WATCH", "WARNING", "DANGER"}
                or not isinstance(areas, list)
                or len(areas) > 3
                or any(not isinstance(area, str) or not area.strip() or len(area) > 100 for area in areas)
            ):
                self.send_json(400, {"error": "Alert data is invalid. Run a new prediction and try again."})
                return
            safe_location = re.sub(r"[\r\n\x00-\x1f\x7f]", " ", location).strip()[:120]
            safe_areas = ", ".join(re.sub(r"[\r\n\x00-\x1f\x7f]", " ", area).strip() for area in areas) or "No significant inundation area in this demo prediction"
            normalized_alert = {
                "rainfall": f"{float(rainfall):g}",
                "risk": risk,
                "risk_level": risk_level,
                "forecast": ", ".join(f"{float(value):g}" for value in forecast),
                "areas": safe_areas,
            }
            alert_message = format_demo_alert_message(safe_location, normalized_alert)
            alert_variables = alert_template_variables(safe_location, normalized_alert)
        unconfigured_channels = [item for item in requested_channels if not channel_is_configured(item)]
        if unconfigured_channels:
            channel_errors = [channel_configuration_error(item) for item in unconfigured_channels]
            self.send_json(
                503,
                {"error": " ".join(error for error in channel_errors if error)},
            )
            return

        weather_message = None
        weather_variables = None
        weather_place = None
        weather_current = None
        if is_weather_message:
            try:
                weather_place, weather_current = fetch_current_weather(location)
                weather_message = format_weather_message(weather_place, weather_current)
                weather_variables = weather_template_variables(weather_place, weather_current)
            except ValueError as error:
                self.send_json(400, {"error": str(error)})
                return
            except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError):
                self.send_json(502, {"error": "Could not retrieve current weather right now. Try again shortly."})
                return

        deliveries: list[dict[str, str]] = []
        failures: list[dict[str, str]] = []
        for requested_channel in requested_channels:
            rate_key = (requested_channel, recipient)
            now = time.monotonic()
            with _last_sent_lock:
                last_sent = _last_sent.get(rate_key, 0)
                if now - last_sent < RATE_LIMIT_SECONDS:
                    failures.append(
                        {
                            "channel": requested_channel,
                            "reason": "rate_limited",
                            "error": "Wait 30 seconds before sending to this recipient on this channel again.",
                        }
                    )
                    continue
                _last_sent[rate_key] = now

            try:
                if requested_channel == "Email":
                    if alert_message is None:
                        raise ValueError("Email is only available for Rainwatch flood alerts.")
                    result = send_email_alert(recipient, location, alert_message)
                else:
                    result = send_twilio_message(
                        requested_channel,
                        recipient,
                        location,
                        message=alert_message if is_alert else weather_message,
                        content_variables=alert_variables if is_alert else weather_variables,
                        content_sid=(
                            os.environ.get("TWILIO_WHATSAPP_WEATHER_CONTENT_SID")
                            if is_weather_message and requested_channel == "WhatsApp"
                            else None
                        ),
                    )
            except HTTPError as error:
                with _last_sent_lock:
                    _last_sent.pop(rate_key, None)
                try:
                    provider_error = json.loads(error.read().decode("utf-8"))
                    code = provider_error.get("code")
                    provider_message = provider_error.get("message")
                except (json.JSONDecodeError, UnicodeDecodeError):
                    code = None
                    provider_message = None
                details = []
                if isinstance(provider_message, str) and provider_message.strip():
                    details.append(re.sub(r"[\r\n\x00-\x1f\x7f]", " ", provider_message).strip()[:400])
                if code:
                    details.append(f"Twilio error code {code}")
                detail = " ".join(details) or "Check your sender configuration, recipient permissions, and WhatsApp template approval."
                failures.append({"channel": requested_channel, "reason": "provider_rejected", "error": f"Twilio rejected {requested_channel}: {detail}"})
            except (TimeoutError, URLError, OSError, smtplib.SMTPException) as error:
                with _last_sent_lock:
                    _last_sent.pop(rate_key, None)
                detail = re.sub(r"[\r\n\x00-\x1f\x7f]", " ", str(error)).strip()[:400]
                message = f"Gmail SMTP error: {detail}" if requested_channel == "Email" and detail else (
                    "Could not reach Gmail SMTP. Check the server internet connection and try again."
                    if requested_channel == "Email"
                    else "Could not reach Twilio. Check the server internet connection and try again."
                )
                failures.append(
                    {
                        "channel": requested_channel,
                        "reason": "provider_error",
                        "error": message,
                    }
                )
            except (KeyError, ValueError) as error:
                with _last_sent_lock:
                    _last_sent.pop(rate_key, None)
                detail = str(error) if isinstance(error, ValueError) else "The provider returned an unreadable response."
                failures.append(
                    {
                        "channel": requested_channel,
                        "reason": "invalid_provider_response",
                        "error": detail,
                    }
                )
            else:
                deliveries.append(
                    {
                        "channel": requested_channel,
                        "status": result["status"],
                        "sid": result["sid"],
                    }
                )

        if not deliveries:
            only_rate_limited = failures and all(failure["reason"] == "rate_limited" for failure in failures)
            error_message = failures[0]["error"] if len(failures) == 1 else "No selected channel accepted the message."
            self.send_json(429 if only_rate_limited else 502, {"error": error_message, "failures": failures})
            return

        if not is_weather_message:
            delivery = deliveries[0]
            self.send_json(
                200,
                {
                    "ok": True,
                    "channel": delivery["channel"],
                    "status": delivery["status"],
                    "sid": delivery["sid"],
                    "location": location,
                },
            )
            return

        response_payload: dict[str, object] = {"ok": not failures, "deliveries": deliveries}
        if is_weather_message and weather_current is not None:
            response_payload.update(
                {
                    "place": weather_place,
                    "condition": WEATHER_CODES.get(int(weather_current["weather_code"]), "Current conditions"),
                    "temperature": weather_current["temperature_2m"],
                    "observedAt": weather_current["time"],
                }
            )
        if failures:
            response_payload["partial"] = True
            response_payload["failures"] = failures
            self.send_json(207, response_payload)
        else:
            self.send_json(200, response_payload)


def main() -> None:
    load_local_env()
    host = "127.0.0.1"
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer((host, port), RainwatchHandler)
    print(f"Rainwatch running at http://localhost:{port}/")
    print("Real alerts require Twilio and/or Gmail SMTP credentials in .env.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Rainwatch server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
