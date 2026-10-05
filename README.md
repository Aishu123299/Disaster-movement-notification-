# Rainwatch India-wide flood-warning demo

Rainwatch is a self-contained Smart India Hackathon demonstration of rainfall early warning and flood-inundation prediction. Its nationwide selector covers all 28 Indian states and 8 union territories, with a city/district list for each. Choose a location and run a simulated prediction to update the dashboard, forecast, risk level, affected-area map, and sample inundation zones.

## Live heavy-rain monitoring

In **Send a Rainwatch alert**, choose **REAL DELIVERY**, select Email, SMS, or WhatsApp, and enter the recipient. In **Monitor every listed city and district**, explicitly consent to ongoing notifications and select **Start Live Monitoring**. Rainwatch checks all 131 city/district coordinates across the 28 states and 8 union territories immediately and then every five minutes while the page remains open. Open-Meteo returns up to 20 locations per batched API request, so the India-wide scan uses seven weather requests per poll. Each location shows trailing 24-hour rainfall and progress toward **64.5 mm**, the IMD heavy-rain threshold amount; forecast rain for the next hour; estimated time (IST) until the first forecast hour with rain; the peak forecast hourly amount/time; and the first forecast hour when the rolling 24-hour model total reaches the threshold, if it is forecast within 24 hours. These are model estimates, not IMD rain-gauge observations, validated flood predictions, or official warnings. Use official IMD and local-authority alerts for safety decisions.

Real alert delivery requires the relevant local Twilio/Gmail `.env` configuration below. Email and SMS can use the existing alert setup. WhatsApp requires a separate approved template for live alerts; configure `TWILIO_WHATSAPP_LIVE_CONTENT_SID` and use this template body:

	```
	RAINWATCH HEAVY RAIN ALERT
	{{1}}
	Current rolling 24-hour rainfall estimate: {{2}} mm.
	Heavy-rain threshold: {{3}} mm/24h.
	{{4}}
	This is an Open-Meteo model estimate/forecast, not an official IMD observation or warning. Follow IMD and local authorities for official guidance.
	```

	The template variables are location, current rolling 24-hour rainfall estimate, threshold, and whether the estimate already meets the threshold or forecasts when it may be reached. Rainwatch attempts an alert when a location is currently at/above the threshold or forecasts the rolling 24-hour total to cross it within 24 hours. It sends at most one alert per recipient/channel/city during that event; it can alert again after the current amount and forecast both fall below threshold and a new crossing is forecast. If many locations qualify, each may produce a separate message. Missing delivery credentials do not stop weather readings; the dashboard shows configuration and provider errors and does not claim messages were sent. The delivery channel and recipient are locked while monitoring is active; stop the monitor to change them. Monitoring stops if you withdraw consent, close/reload the page, or stop the local server. Changing the dashboard's selected city does not affect the India-wide scan. Duplicate suppression is held in server memory and resets when the server restarts. Do not leave the demo unattended as a life-safety service.

## Dashboard data

The dashboard uses deterministic, realistic **DEMO DATA** for rainfall, temperature, humidity, river level, forecast, and flood risk so the presentation works without weather API, Twilio, or SMTP credentials. The default Pune scenario displays 78 mm rainfall and high flood risk. The interactive map uses OpenStreetMap tiles when online and redraws the selected city and illustrative risk overlays after each prediction. Rainfall and water-level charts are simulated model visualizations, not observations. Predicted inundation areas are illustrative; this site does not provide a real forecast, validated AI/ML output, official warning, or evacuation plan. Always follow IMD and local authorities for emergencies.

## Configure real Twilio alerts

1. Create or use a Twilio account and configure an SMS-capable sender and/or a WhatsApp sender.
2. Copy `.env.example` to `.env` in this folder.
3. Fill in `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and the sender value for each channel you want to use. Keep `.env` private; it is ignored by Git.
4. For WhatsApp, create and get approval for a Twilio Content Template with this body, then set its `HX...` Content SID as `TWILIO_WHATSAPP_CONTENT_SID`:

	```
	RAINWATCH FLOOD ALERT for {{1}}.
	DEMO DATA — simulated prediction, NOT an official warning.
	Rainfall: {{2}} mm. Flood risk: {{3}} ({{4}}).
	Next 3-hour rainfall forecast: {{5}} mm/hr.
	Predicted inundation areas: {{6}}.
	{{7}}
	Generated: {{8}}.
	```

	The template variables are location, demo rainfall, risk, risk level, next-three-hour rainfall forecast, predicted inundation areas, safety guidance, and generation time. WhatsApp messages require an approved template. The legacy `/api/weather-message` endpoint uses this SID by default; to keep a separate current-weather template, set its approved SID in the optional `TWILIO_WHATSAPP_WEATHER_CONTENT_SID` setting.
5. For the Twilio WhatsApp Sandbox, use the sender shown in your Twilio console and have the recipient join the sandbox using its join instructions. The recipient must opt in. The recipient must also have consented to receive the alert.
6. For trial accounts, verify the recipient number in Twilio. SMS delivery in India may also require an approved sender and DLT/template registration.

Do not paste account credentials or authentication tokens into chat or the browser.

## Configure real Gmail email alerts

1. In your Google Account, enable 2-Step Verification and create an App Password for Rainwatch. Google does not accept your regular account password for this SMTP login.
2. Copy `.env.example` to `.env` if you have not already done so. Set `SMTP_USERNAME` to the sending Gmail address and `SMTP_PASSWORD` to its App Password. Keep the App Password private.
3. Keep `SMTP_HOST=smtp.gmail.com` and `SMTP_PORT=587`; optionally set `SMTP_FROM` to the same authorized sender address.
4. Restart `python server.py`. In **Send a Rainwatch alert**, choose **REAL DELIVERY**, select **Email**, enter the recipient email address, and explicitly consent before sending.

The SMTP password remains server-side. The app reports success only after Gmail SMTP accepts the email for sending; SMTP acceptance does not guarantee delivery to the recipient's inbox. Setup and SMTP provider errors are shown to the user. DEMO MODE continues to simulate locally without contacting a recipient.

## Start

From this folder, run:

```powershell
python server.py
```

Then open http://localhost:8000/. The server binds to `127.0.0.1`, so it only accepts connections from this computer. Twilio and Email credentials remain on the server.

## Send an alert

In **Send a Rainwatch alert**, choose **REAL DELIVERY**, select Email or a Twilio channel, enter the recipient (E.164 format for SMS/WhatsApp, email address for Email), enter the location, and explicitly consent before sending. The browser posts to the local `/api/alert` endpoint; provider credentials are read by the server from `.env` and are never sent to the browser. Rainwatch displays success only after Twilio accepts the request and returns a message SID, or Gmail SMTP accepts the email. Provider/setup errors are shown without claiming delivery. Provider acceptance is not confirmation that a message reached a handset or inbox.

Manually sent alerts from **Send a Rainwatch alert** contain the simulated dashboard prediction and are clearly labeled **DEMO DATA — simulated prediction, NOT an official warning**. Automated live-monitor alerts are based on Open-Meteo model rainfall estimates and explicitly disclose that source; they are not verified observations or official warnings. Do not use Rainwatch values instead of official emergency guidance.

To test without contacting anyone, choose **DEMO MODE**. It shows an explicitly simulated local notification and does not call Twilio. The separate alert-preview form is also local-only.

## Run locally

Run `python server.py` from this folder and open http://localhost:8000/. Demo predictions work without credentials. Real delivery requires `.env` setup and a server restart after editing credentials.
