const placesByState = {
  'Andaman and Nicobar Islands': ['Port Blair|11.6234|92.7265', 'Car Nicobar|9.152|92.819', 'Havelock Island|12.016|92.987'],
  'Andhra Pradesh': ['Visakhapatnam|17.6868|83.2185', 'Vijayawada|16.5062|80.648', 'Amaravati|16.5745|80.3598', 'Tirupati|13.6288|79.4192', 'Kurnool|15.8281|78.0373'],
  'Arunachal Pradesh': ['Itanagar|27.0844|93.6053', 'Tawang|27.5861|91.8594', 'Pasighat|28.0669|95.3267'],
  Assam: ['Guwahati|26.1445|91.7362', 'Silchar|24.8333|92.7789', 'Dibrugarh|27.4728|94.912', 'Jorhat|26.7509|94.2037'],
  Bihar: ['Patna|25.5941|85.1376', 'Gaya|24.7914|85.0002', 'Muzaffarpur|26.1209|85.3647', 'Bhagalpur|25.2425|86.9842'],
  Chandigarh: ['Chandigarh|30.7333|76.7794'],
  Chhattisgarh: ['Raipur|21.2514|81.6296', 'Bilaspur|22.0797|82.1409', 'Jagdalpur|19.0748|82.008'],
  'Dadra and Nagar Haveli and Daman and Diu': ['Daman|20.3974|72.8328', 'Silvassa|20.2763|73.0083', 'Diu|20.7144|70.9874'],
  Delhi: ['New Delhi|28.6139|77.209', 'Dwarka|28.5921|77.046', 'North Delhi|28.7041|77.1025'],
  Goa: ['Panaji|15.4909|73.8278', 'Margao|15.2832|73.9862', 'Vasco da Gama|15.386|73.8441'],
  Gujarat: ['Ahmedabad|23.0225|72.5714', 'Surat|21.1702|72.8311', 'Vadodara|22.3072|73.1812', 'Rajkot|22.3039|70.8022', 'Bhuj|23.241|69.6669'],
  Haryana: ['Gurugram|28.4595|77.0266', 'Faridabad|28.4089|77.3178', 'Hisar|29.1492|75.7217', 'Panipat|29.3909|76.9635'],
  'Himachal Pradesh': ['Shimla|31.1048|77.1734', 'Dharamshala|32.219|76.3234', 'Mandi|31.708|76.932'],
  'Jammu and Kashmir': ['Srinagar|34.0837|74.7973', 'Jammu|32.7266|74.857', 'Anantnag|33.7311|75.1487', 'Baramulla|34.209|74.3429'],
  Jharkhand: ['Ranchi|23.3441|85.3096', 'Jamshedpur|22.8046|86.2029', 'Dhanbad|23.7957|86.4304', 'Deoghar|24.4855|86.6947'],
  Karnataka: ['Bengaluru|12.9716|77.5946', 'Mysuru|12.2958|76.6394', 'Mangaluru|12.9141|74.856', 'Hubballi|15.3647|75.124', 'Belagavi|15.8497|74.4977'],
  Kerala: ['Kochi|9.9312|76.2673', 'Thiruvananthapuram|8.5241|76.9366', 'Kozhikode|11.2588|75.7804', 'Thrissur|10.5276|76.2144', 'Wayanad|11.6854|76.132'],
  Ladakh: ['Leh|34.1526|77.5771', 'Kargil|34.5539|76.1349'],
  Lakshadweep: ['Kavaratti|10.5667|72.6417', 'Agatti|10.856|72.195'],
  'Madhya Pradesh': ['Bhopal|23.2599|77.4126', 'Indore|22.7196|75.8577', 'Jabalpur|23.1815|79.9864', 'Gwalior|26.2183|78.1828', 'Ujjain|23.1765|75.7885'],
  Maharashtra: ['Mumbai|19.076|72.8777', 'Pune|18.5204|73.8567', 'Nagpur|21.1458|79.0882', 'Nashik|19.9975|73.7898', 'Kolhapur|16.705|74.2433', 'Chhatrapati Sambhajinagar|19.8762|75.3433'],
  Manipur: ['Imphal|24.817|93.9368', 'Churachandpur|24.3335|93.6834', 'Thoubal|24.638|94.0106'],
  Meghalaya: ['Shillong|25.5788|91.8933', 'Tura|25.5142|90.2039', 'Cherrapunji|25.2702|91.7323'],
  Mizoram: ['Aizawl|23.7271|92.7176', 'Lunglei|22.887|92.734'],
  Nagaland: ['Kohima|25.6751|94.1086', 'Dimapur|25.8629|93.7537', 'Mokokchung|26.322|94.517'],
  Odisha: ['Bhubaneswar|20.2961|85.8245', 'Cuttack|20.4625|85.883', 'Puri|19.8135|85.8312', 'Sambalpur|21.4669|83.9812'],
  Puducherry: ['Puducherry|11.9416|79.8083', 'Karaikal|10.9254|79.838'],
  Punjab: ['Amritsar|31.634|74.8723', 'Ludhiana|30.901|75.8573', 'Jalandhar|31.326|75.5762', 'Patiala|30.3398|76.3869'],
  Rajasthan: ['Jaipur|26.9124|75.7873', 'Jodhpur|26.2389|73.0243', 'Udaipur|24.5854|73.7125', 'Kota|25.2138|75.8648', 'Bikaner|28.0229|73.3119'],
  Sikkim: ['Gangtok|27.3389|88.6065', 'Namchi|27.1667|88.3667', 'Gyalshing|27.2895|88.2636'],
  'Tamil Nadu': ['Chennai|13.0827|80.2707', 'Coimbatore|11.0168|76.9558', 'Madurai|9.9252|78.1198', 'Tiruchirappalli|10.7905|78.7047', 'Tirunelveli|8.7139|77.7567'],
  Telangana: ['Hyderabad|17.385|78.4867', 'Warangal|17.9689|79.5941', 'Nizamabad|18.6725|78.0941', 'Khammam|17.2473|80.1514'],
  Tripura: ['Agartala|23.8315|91.2868', 'Udaipur|23.533|91.483', 'Dharmanagar|24.3667|92.1667'],
  'Uttar Pradesh': ['Lucknow|26.8467|80.9462', 'Varanasi|25.3176|82.9739', 'Kanpur|26.4499|80.3319', 'Prayagraj|25.4358|81.8463', 'Agra|27.1767|78.0081', 'Gorakhpur|26.7606|83.3732'],
  Uttarakhand: ['Dehradun|30.3165|78.0322', 'Haridwar|29.9457|78.1642', 'Haldwani|29.2183|79.513'],
  'West Bengal': ['Kolkata|22.5726|88.3639', 'Howrah|22.5958|88.2636', 'Siliguri|26.7271|88.3953', 'Durgapur|23.5204|87.3119']
};

const riskLevels = ['NORMAL', 'WATCH', 'WARNING', 'DANGER'];
const citySelect = document.getElementById('city-select');
const stateSelect = document.getElementById('state-select');
const mapElement = document.getElementById('map');
let map;
let rainOverlay;
let floodOverlay;
let predictionRun = 0;
let activeLocation;
let currentScenario;
let liveMonitorTimer;
let liveMonitorActive = false;
let liveMonitorCheckInProgress = false;
let liveMonitorDelivery;

function getPlaceRecords(state) {
  return (placesByState[state] || []).map((entry) => {
    const [name, latitude, longitude] = entry.split('|');
    return { name, latitude: Number(latitude), longitude: Number(longitude) };
  });
}

function getAllPlaceRecords() {
  return Object.entries(placesByState).flatMap(([state, entries]) =>
    entries.map((entry) => {
      const [name, latitude, longitude] = entry.split('|');
      return {
        id: `${state}:${name}`,
        name,
        state,
        latitude: Number(latitude),
        longitude: Number(longitude)
      };
    })
  );
}

function getSelectedLocation() {
  const state = stateSelect.value;
  const place = getPlaceRecords(state).find((item) => item.name === citySelect.value);
  return place ? { ...place, state } : null;
}

function hashLocation(location) {
  return `${location.state}:${location.name}`.split('').reduce((hash, character) => (hash * 31 + character.charCodeAt(0)) >>> 0, 7);
}

function getScenario(location, runNumber = 0) {
  const hash = hashLocation(location);
  const rainfallBase = location.state === 'Maharashtra' && location.name === 'Pune'
    ? 78
    : 14 + (hash % 79);
  const variance = [0, -3, 2, -1][runNumber % 4];
  const rainfall = Math.max(5, rainfallBase + variance);
  const levelIndex = rainfall >= 70 ? 3 : rainfall >= 50 ? 2 : rainfall >= 28 ? 1 : 0;
  const level = riskLevels[levelIndex];
  const risk = levelIndex >= 2 ? 'HIGH' : levelIndex === 1 ? 'MODERATE' : 'LOW';
  const offset = ((hash % 13) - 6) / 10;
  const climateAdjustment = {
    Ladakh: -16,
    'Himachal Pradesh': -8,
    'Jammu and Kashmir': -9,
    Uttarakhand: -5,
    Sikkim: -6,
    'Arunachal Pradesh': -4,
    Meghalaya: -3,
    Rajasthan: 3,
    Gujarat: 2
  }[location.state] || 0;
  const temperature = Math.max(8, Math.min(39, 27 - Math.abs(location.latitude - 20) * 0.16 + climateAdjustment + offset));
  const water = (2.45 + levelIndex * 0.64 + rainfall / 100 + (hash % 7) / 20).toFixed(1);
  const areaCount = [1, 1, 2, 3][levelIndex];
  const areaLabels = [
    `Low-lying wards around ${location.name}`,
    `Urban drainage corridors · ${location.name}`,
    `River-adjacent and floodplain areas · ${location.name}`
  ];
  return {
    level,
    levelIndex,
    risk,
    probability: Math.min(96, [16, 43, 71, 86][levelIndex] + hash % 5),
    rainfall,
    temperature: temperature.toFixed(1),
    humidity: 58 + hash % 30,
    water,
    forecast: [
      Math.max(2, Math.round(rainfall * 0.40)),
      Math.max(2, Math.round(rainfall * 0.48)),
      Math.max(2, Math.round(rainfall * 0.37))
    ],
    areas: areaLabels.slice(0, areaCount),
    location
  };
}

function updateClock() {
  const now = new Date();
  const timeParts = new Intl.DateTimeFormat('en-GB', {
    hour: '2-digit',
    minute: '2-digit',
    hourCycle: 'h23',
    timeZone: 'Asia/Kolkata'
  }).formatToParts(now);
  const hour = Number(timeParts.find((part) => part.type === 'hour').value);
  const minute = timeParts.find((part) => part.type === 'minute').value;
  document.getElementById('current-time').textContent = `${String(hour).padStart(2, '0')}:${minute} IST`;
  document.getElementById('current-date').textContent = new Intl.DateTimeFormat('en-IN', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    timeZone: 'Asia/Kolkata'
  }).format(now).toUpperCase();
}

function makeRiskCircle(center, radius, color, fillOpacity, label) {
  return L.circle(center, {
    radius,
    color,
    weight: 1.5,
    opacity: 0.8,
    fillColor: color,
    fillOpacity
  }).bindTooltip(label, { direction: 'top', sticky: true });
}

function initializeMap() {
  if (!window.L || !mapElement) {
    mapElement.innerHTML = '<div class="map-fallback">Map tiles are unavailable. Restart or refresh the demo when a network connection is available.</div>';
    return;
  }
  map = L.map(mapElement, { scrollWheelZoom: false, zoomControl: true }).setView([18.525, 73.865], 12);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);
  rainOverlay = L.layerGroup().addTo(map);
  floodOverlay = L.layerGroup().addTo(map);
  window.setTimeout(() => map.invalidateSize(), 150);
}

function renderScenario(scenario, isPrediction) {
  currentScenario = scenario;
  const { location } = scenario;
  const areaName = `${location.name}, ${location.state}`;
  document.getElementById('dashboard-location').textContent = areaName;
  document.getElementById('weather-place').textContent = areaName;
  document.querySelector('.page-subtitle').textContent = `AI-assisted rainfall and inundation outlook for ${areaName}.`;
  document.querySelector('.panel-heading .section-kicker').textContent = `${location.name.toUpperCase()} · ${location.state.toUpperCase()}`;
  document.querySelector('.metric-card.rainfall-card .metric-label').textContent = 'CURRENT RAINFALL · DEMO DATA';
  document.getElementById('rainfall-value').textContent = String(scenario.rainfall);
  document.querySelector('.metric-card.rainfall-card .trend-chip').textContent = scenario.rainfall >= 50 ? '↑ HEAVY' : scenario.rainfall >= 28 ? '↑ RISING' : 'STEADY';
  document.getElementById('temperature-value').textContent = scenario.temperature;
  document.getElementById('condition-value').textContent = scenario.rainfall >= 50 ? 'Heavy rainfall · demo' : scenario.rainfall >= 28 ? 'Moderate rain · demo' : 'Showers · demo';
  document.getElementById('humidity-value').textContent = String(scenario.humidity);
  document.getElementById('rainfall-context').textContent = 'SIMULATED · 3-hour total';
  document.getElementById('wind-value').textContent = String(8 + hashLocation(location) % 19);
  document.getElementById('risk-value').textContent = scenario.risk;
  document.getElementById('risk-level').textContent = scenario.level;
  document.getElementById('risk-probability').textContent = `${scenario.probability}% demo likelihood`;
  document.getElementById('risk-track').style.width = `${scenario.probability}%`;
  document.getElementById('water-level-value').textContent = scenario.water;
  document.querySelector('.metric-card.river-card .metric-label').textContent = `WATER LEVEL · ${location.name.toUpperCase()}`;
  document.getElementById('risk-value').dataset.level = scenario.level.toLowerCase();
  document.getElementById('risk-level').dataset.level = scenario.level.toLowerCase();
  document.getElementById('prediction-risk').textContent = scenario.risk;
  document.getElementById('prediction-risk').dataset.level = scenario.level.toLowerCase();
  document.getElementById('prediction-confidence').textContent = `${scenario.probability}% demo confidence · next 3 hours`;
  document.getElementById('prediction-status').textContent = isPrediction ? 'PREDICTION COMPLETE · DEMO' : 'DEMO SCENARIO · READY';
  document.getElementById('prediction-detail').textContent = scenario.levelIndex >= 2
    ? `Heavy rainfall may cause localized inundation in ${scenario.areas[0].toLowerCase()} and connected drainage corridors.`
    : scenario.levelIndex === 1
      ? `Monitor rainfall and drainage in ${scenario.areas[0].toLowerCase()}; risk may increase if rain persists.`
      : `No significant demo inundation is predicted for ${location.name}; continue routine monitoring.`;
  document.getElementById('prediction-updated').textContent = `SIMULATED MODEL OUTPUT · ${areaName}`;
  document.getElementById('forecast-summary').textContent = scenario.levelIndex >= 2
    ? `Heavy rain continues around ${location.name}`
    : scenario.levelIndex === 1
      ? `Rain may intensify around ${location.name}`
      : `Light rainfall expected around ${location.name}`;
  document.getElementById('headline-alert').textContent = scenario.levelIndex >= 2
    ? `Heavy rainfall detected. Flood risk is ${scenario.risk}.`
    : `Rainfall monitoring active. Flood risk is ${scenario.risk}.`;
  document.getElementById('alert-guidance').textContent = scenario.levelIndex >= 2
    ? `DEMO DATA for ${areaName}. Please move to a safe area. Follow local authorities for official emergency guidance.`
    : `DEMO DATA for ${areaName}. Stay informed and follow local authorities for official emergency guidance.`;
  document.querySelectorAll('.chart-col .forecast-bar').forEach((bar, index) => {
    bar.style.height = `${Math.max(12, Math.min(100, scenario.forecast[index] / 40 * 100))}%`;
    bar.setAttribute('aria-label', `${scenario.forecast[index]} millimeters`);
  });
  document.querySelectorAll('.chart-col .forecast-bar + span').forEach((label, index) => {
    label.textContent = `+${index + 1}h`;
  });
  document.querySelector('.hourly-chart').setAttribute(
    'aria-label',
    `Demo rainfall forecast: ${scenario.forecast.join(', ')} millimeters per hour for the next three hours`
  );
  renderAffectedAreas(scenario);
  renderTrendCharts(scenario);
  renderRiskLegend(scenario);
  updateFloodMap(scenario);
  document.getElementById('location-picker-status').textContent = isPrediction
    ? `PREDICTION UPDATED · ${areaName}`
    : `DEMO DATA · ${areaName}`;
  if (map) map.flyTo([location.latitude, location.longitude], 12, { duration: 0.6 });
  document.getElementById('simulation-location').value = areaName;
  document.getElementById('delivery-location').value = areaName;
  document.getElementById('user-location').value = areaName;
}

function renderAffectedAreas(scenario) {
  const list = document.getElementById('affected-area-list');
  list.replaceChildren();
  document.getElementById('affected-count').textContent = String(scenario.areas.length);
  scenario.areas.forEach((area, index) => {
    const item = document.createElement('li');
    const icon = document.createElement('span');
    icon.className = 'safe-icon';
    icon.textContent = scenario.levelIndex >= 2 ? '!' : '·';
    const description = document.createElement('span');
    const name = document.createElement('strong');
    const detail = document.createElement('small');
    name.textContent = area;
    detail.textContent = `${index === 0 ? 'Predicted inundation zone' : index === 1 ? 'Urban drainage hotspot' : 'Low-lying floodplain'} · DEMO DATA`;
    description.append(name, detail);
    const arrow = document.createElement('span');
    arrow.className = 'safe-arrow';
    arrow.textContent = '↗';
    item.append(icon, description, arrow);
    list.append(item);
  });
}

function renderRiskLegend(scenario) {
  document.querySelectorAll('.risk-legend span').forEach((item, index) => {
    item.classList.toggle('active', index === scenario.levelIndex);
  });
}

function renderTrendCharts(scenario) {
  const { rainfall, water, forecast } = scenario;
  const rainPoints = [
    Math.max(16, Math.min(132, 134 - rainfall * 0.29)),
    Math.max(15, Math.min(132, 132 - rainfall * 0.48)),
    Math.max(14, Math.min(132, 130 - rainfall * 0.72)),
    Math.max(12, Math.min(132, 130 - rainfall * 0.94)),
    Math.max(10, Math.min(132, 129 - rainfall * 1.13)),
    Math.max(10, Math.min(132, 130 - rainfall * 1.28)),
    Math.max(10, Math.min(132, 128 - Math.max(...forecast) * 1.8))
  ];
  const waterNumber = Number(water);
  const waterPoints = [5.9, 5.7, 5.5, 5.25, 5.0, 4.65, waterNumber].map(
    (value) => Math.max(12, Math.min(135, 145 - value * 21))
  );
  updateSvgTrend('.rainfall-trend', rainPoints);
  updateSvgTrend('.water-trend', waterPoints);
  document.querySelector('.rainfall-trend').setAttribute(
    'aria-label',
    `DEMO rainfall trend for ${scenario.location.name}. Three-hour rainfall ${rainfall} millimeters, followed by forecast of ${forecast.join(', ')} millimeters per hour`
  );
  document.querySelector('.water-trend').setAttribute(
    'aria-label',
    `DEMO water-level trend for ${scenario.location.name}, currently ${water} meters`
  );
  document.querySelector('.water-trend').previousElementSibling.querySelector('.section-kicker').textContent =
    `DEMO WATER GAUGE · ${scenario.location.name.toUpperCase()}`;
}

function updateSvgTrend(selector, points) {
  const plot = document.querySelector(selector);
  const coordinates = points.map((y, index) => `${index * 100},${Math.round(y)}`).join(' ');
  const line = plot.querySelector('polyline');
  const area = plot.querySelector('path');
  line.setAttribute('points', coordinates);
  area.setAttribute('d', `M${coordinates.replaceAll(' ', ' L')} L600 150 L0 150 Z`);
}

function updateFloodMap(scenario) {
  if (!map || !floodOverlay || !rainOverlay) return;
  const { location } = scenario;
  const palette = [
    { color: '#5caa7a', opacity: 0.12, radius: 550 },
    { color: '#dbb248', opacity: 0.2, radius: 800 },
    { color: '#dc8a43', opacity: 0.28, radius: 1050 },
    { color: '#d35c42', opacity: 0.36, radius: 1300 }
  ][scenario.levelIndex];
  rainOverlay.clearLayers();
  rainOverlay.addLayer(makeRiskCircle(
    [location.latitude, location.longitude],
    2500 + scenario.rainfall * 32,
    '#38a6ae',
    0.19,
    `DEMO rainfall footprint · ${scenario.rainfall} mm · ${location.name}`
  ));
  rainOverlay.addLayer(makeRiskCircle(
    [location.latitude + 0.025, location.longitude + 0.025],
    1600 + scenario.rainfall * 20,
    '#40a9a4',
    0.14,
    `DEMO rainfall forecast · ${location.name}`
  ));
  floodOverlay.clearLayers();
  const offsets = [[0.006, 0.009], [0.014, -0.012], [-0.012, 0.016]];
  scenario.areas.forEach((area, index) => {
    const center = [location.latitude + offsets[index][0], location.longitude + offsets[index][1]];
    floodOverlay.addLayer(makeRiskCircle(center, palette.radius, palette.color, palette.opacity, `${area} · ${scenario.level} · DEMO DATA`));
    L.circleMarker(center, { radius: 6, color: '#fff', weight: 2, fillColor: palette.color, fillOpacity: 1 })
      .addTo(floodOverlay)
      .bindTooltip(`${area} · ${scenario.level} risk · simulated inundation`);
  });
  L.circleMarker([location.latitude, location.longitude], {
    radius: 7,
    color: '#fff',
    weight: 2,
    fillColor: '#176e66',
    fillOpacity: 1
  }).addTo(floodOverlay).bindTooltip(`${location.name}, ${location.state} · selected demo location`);
}

function populateStates() {
  const states = Object.keys(placesByState).sort((first, second) => first.localeCompare(second));
  states.forEach((state) => {
    const option = document.createElement('option');
    option.value = state;
    option.textContent = state;
    stateSelect.append(option);
  });
  stateSelect.value = 'Maharashtra';
  populateCities('Pune');
}

function populateCities(selectedCity) {
  const records = getPlaceRecords(stateSelect.value);
  citySelect.replaceChildren();
  records.forEach((place) => {
    const option = document.createElement('option');
    option.value = place.name;
    option.textContent = place.name;
    citySelect.append(option);
  });
  citySelect.value = records.some((place) => place.name === selectedCity) ? selectedCity : records[0].name;
}

function runPrediction() {
  const location = getSelectedLocation();
  if (!location) return;
  predictionRun += 1;
  renderScenario(getScenario(location, predictionRun), true);
  document.getElementById('prediction-updated').textContent =
    `PREDICTION #${predictionRun} · SIMULATED MODEL · ${location.name}, ${location.state}`;
}

function currentAlertMessage(location, scenario) {
  return `DEMO DATA — ${scenario.rainfall} mm rainfall in ${location.name}, ${location.state}. Flood risk is ${scenario.risk} (${scenario.level}). Please move to a safe area. This is simulated data, not an official warning.`;
}

function showAlertNotice(text) {
  const notice = document.getElementById('demo-toast');
  notice.textContent = text;
  notice.hidden = false;
  notice.focus();
  window.setTimeout(() => {
    notice.hidden = true;
  }, 10000);
}

function showDemoAlert(phone, channels, location) {
  const alertLocation = location.trim() || `${activeLocation.name}, ${activeLocation.state}`;
  const channelNames = channels.join(' + ');
  const message = currentAlertMessage(activeLocation, currentScenario);
  const text = `✓ DEMO ALERT SUCCESSFULLY SIMULATED\n${channelNames} · ${phone}\n${alertLocation}\n${message}\nNo real message was sent.`;
  showAlertNotice(text);
  return text;
}

populateStates();
initializeMap();
activeLocation = getSelectedLocation();
currentScenario = getScenario(activeLocation);
renderScenario(currentScenario, false);
updateClock();
window.setInterval(updateClock, 30000);

stateSelect.addEventListener('change', () => {
  populateCities();
  const location = getSelectedLocation();
  activeLocation = location;
  document.getElementById('location-picker-status').textContent = `SELECTION READY · ${location.name}, ${location.state}`;
});

citySelect.addEventListener('change', () => {
  const location = getSelectedLocation();
  activeLocation = location;
  document.getElementById('location-picker-status').textContent = `SELECTION READY · ${location.name}, ${location.state}`;
});

document.getElementById('run-prediction-top').addEventListener('click', runPrediction);
document.getElementById('run-prediction').addEventListener('click', runPrediction);

for (const control of document.querySelectorAll('.map-filter')) {
  control.addEventListener('click', () => {
    const selected = control.classList.toggle('selected');
    control.setAttribute('aria-pressed', String(selected));
    if (!map) return;
    const layer = control.dataset.layer === 'rain' ? rainOverlay : floodOverlay;
    if (selected) layer.addTo(map);
    else map.removeLayer(layer);
  });
}

document.getElementById('refresh-button').addEventListener('click', () => {
  runPrediction();
  document.getElementById('refresh-button').classList.add('spinning');
  if (map) map.invalidateSize();
  window.setTimeout(() => document.getElementById('refresh-button').classList.remove('spinning'), 350);
});

document.getElementById('locate-button').addEventListener('click', () => {
  if (!map || !activeLocation) return;
  map.flyTo([activeLocation.latitude, activeLocation.longitude], 12, { duration: 0.7 });
  document.getElementById('map-section').scrollIntoView({ behavior: 'smooth', block: 'center' });
});

document.getElementById('signup-form').addEventListener('submit', (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const status = document.getElementById('signup-status');
  const digits = form.elements.phone.value.replace(/\D/g, '');
  const location = getSelectedLocation();
  const channels = [...form.querySelectorAll('input[name="channel"]:checked')].map((input) => input.value);
  if (!/^\d{10}$/.test(digits)) {
    status.textContent = 'Enter a valid 10-digit Indian mobile number.';
    return;
  }
  if (!channels.length) {
    status.textContent = 'Select WhatsApp, SMS, or both alert channels.';
    return;
  }
  if (!form.elements.consent.checked) {
    status.textContent = 'Confirm that you want to simulate this demo alert.';
    return;
  }
  activeLocation = location;
  if (location.name !== currentScenario.location.name || location.state !== currentScenario.location.state) {
    predictionRun = 0;
    renderScenario(getScenario(location), true);
  }
  const text = showDemoAlert(`+91${digits}`, channels, form.elements.location.value || `${location.name}, ${location.state}`);
  status.textContent = text;
});

document.getElementById('delivery-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const submitButton = document.getElementById('delivery-submit');
  const status = document.getElementById('provider-status');
  const recipient = form.elements.recipient.value.trim();
  const channel = form.elements.channel.value;
  const location = getSelectedLocation();
  if (!form.reportValidity()) return;
  if (channel !== 'Email' && !/^\+[1-9]\d{7,14}$/.test(recipient)) {
    status.textContent = 'Enter a valid international phone number, for example +919876543210.';
    return;
  }
  if (channel === 'Email' && !/^[^@\s<>]+@[^@\s<>]+\.[^@\s<>]+$/.test(recipient)) {
    status.textContent = 'Enter a valid email address, for example name@gmail.com.';
    return;
  }
  if (form.elements.mode.value === 'real' && !form.elements.consent.checked) {
    status.textContent = 'Confirm consent before sending a real message.';
    return;
  }
  activeLocation = location;
  if (location.name !== currentScenario.location.name || location.state !== currentScenario.location.state) {
    renderScenario(getScenario(location), true);
  }
  const recipientLocation = form.elements.location.value.trim();
  if (form.elements.mode.value === 'demo') {
    const text = showDemoAlert(recipient, [channel], recipientLocation);
    status.textContent = text;
    return;
  }

  submitButton.disabled = true;
  submitButton.textContent = channel === 'Email' ? 'Sending email…' : 'Sending through Twilio…';
  status.textContent = `Sending a real ${channel} alert to ${recipient}…`;
  try {
    const response = await fetch('/api/alert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        channel,
        recipient,
        location: recipientLocation,
        consent: form.elements.consent.checked,
        alert: {
          rainfall: currentScenario.rainfall,
          risk: currentScenario.risk,
          risk_level: currentScenario.level,
          forecast: currentScenario.forecast,
          areas: currentScenario.areas
        }
      })
    });
    const result = await response.json();
    if (!response.ok || result.ok !== true || !result.sid) {
      throw new Error(result.error || `${channel} provider did not confirm accepting the message.`);
    }
    const acceptedBy = channel === 'Email' ? 'Gmail SMTP accepted the email; inbox delivery is not guaranteed.' : `Twilio accepted the message (${result.status}).`;
    const confirmation = `✓ Alert sent successfully\n${result.channel} · ${result.location}\n${acceptedBy} Alert contains DEMO DATA.`;
    status.textContent = confirmation;
    showAlertNotice(confirmation);
  } catch (error) {
    status.textContent = `Alert not sent: ${error.message || 'Could not reach the Rainwatch server.'}`;
  } finally {
    submitButton.disabled = false;
    updateDeliveryMode(false);
  }
});

document.getElementById('contact-form').addEventListener('submit', (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  document.getElementById('contact-status').textContent = 'Thanks for your feedback. This demo does not send it to a service.';
  form.reset();
});

document.getElementById('simulation-form').addEventListener('submit', (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const hazard = form.elements.hazard.value;
  const location = form.elements.location.value.trim();
  document.getElementById('simulation-message').textContent =
    `DEMO DATA — NOT A REAL WARNING\n${hazard} for ${location}.\n${currentAlertMessage(activeLocation, currentScenario)}\nNo live hazard was checked and no message was sent.`;
  document.getElementById('simulation-result').hidden = false;
});

function updateDeliveryChannel() {
  const channel = document.getElementById('delivery-channel').value;
  const recipient = document.getElementById('delivery-recipient');
  const recipientLabel = document.getElementById('delivery-recipient-label');
  if (channel === 'Email') {
    recipient.type = 'email';
    recipient.inputMode = 'email';
    recipient.autocomplete = 'email';
    recipient.placeholder = 'name@gmail.com';
    recipient.removeAttribute('pattern');
    recipientLabel.firstChild.textContent = 'EMAIL ADDRESS';
  } else {
    recipient.type = 'tel';
    recipient.inputMode = 'tel';
    recipient.autocomplete = 'tel';
    recipient.placeholder = '+919876543210';
    recipient.pattern = '\\+[1-9][0-9]{7,14}';
    recipientLabel.firstChild.textContent = 'PHONE NUMBER · E.164';
    if (recipient.value.includes('@')) recipient.value = '';
  }
  document.getElementById('outgoing-preview-label').textContent = `${channel.toUpperCase()} ALERT PREVIEW`;
  document.querySelector('.whatsapp-mark').textContent = channel === 'WhatsApp' ? 'WA' : channel === 'Email' ? '@' : 'SMS';
}

function updateDeliveryMode(showModeStatus = true) {
  const form = document.getElementById('delivery-form');
  const isReal = form.elements.mode.value === 'real';
  const channel = form.elements.channel.value;
  updateDeliveryChannel();
  document.getElementById('delivery-submit').textContent = isReal ? 'Send Real Alert' : 'Preview Demo Alert';
  document.getElementById('delivery-consent').required = isReal;
  if (showModeStatus) {
    document.getElementById('delivery-consent').checked = false;
    document.querySelector('.delivery-consent').lastChild.textContent = isReal
      ? `Authorize one real ${channel} message to this recipient. The alert contains simulated demo data.`
      : 'Preview a DEMO DATA alert locally. No real message will be sent.';
    document.getElementById('provider-status').textContent = isReal
      ? `REAL DELIVERY selected. ${channel === 'Email' ? 'Gmail SMTP' : 'Twilio'} will be contacted only after you consent and send.`
      : 'DEMO MODE selected. No real message will be sent.';
    document.querySelector('.delivery-intro p').textContent = isReal
      ? 'A real message is sent only after consent. The alert clearly identifies its simulated flood data.'
      : 'Preview a simulated alert locally. No recipient or messaging service is contacted.';
  }
  document.getElementById('outgoing-preview-label').textContent =
    `${channel.toUpperCase()} ${isReal ? 'REAL DELIVERY' : 'DEMO MODE'} · PREVIEW`;
}

document.getElementById('delivery-mode').addEventListener('change', updateDeliveryMode);
document.getElementById('delivery-channel').addEventListener('change', updateDeliveryMode);

function stopLiveMonitoring(statusText = 'Live monitoring stopped.') {
  if (liveMonitorTimer) window.clearInterval(liveMonitorTimer);
  liveMonitorTimer = undefined;
  liveMonitorActive = false;
  liveMonitorCheckInProgress = false;
  liveMonitorDelivery = undefined;
  document.getElementById('monitor-consent').checked = false;
  for (const id of ['delivery-mode', 'delivery-channel', 'delivery-recipient']) {
    document.getElementById(id).disabled = false;
  }
  document.getElementById('system-status').textContent = 'DEMO MODE · SIMULATED DATA';
  document.getElementById('live-monitor').classList.remove('is-monitoring');
  document.getElementById('monitor-toggle').innerHTML = 'Start Live Monitoring <span>◉</span>';
  document.getElementById('live-monitor-status').textContent = statusText;
}

async function checkLiveRainfall() {
  if (!liveMonitorActive || liveMonitorCheckInProgress) return false;
  liveMonitorCheckInProgress = true;
  const form = document.getElementById('delivery-form');
  const { channel, recipient } = liveMonitorDelivery;
  const status = document.getElementById('live-monitor-status');
  const locations = getAllPlaceRecords();
  try {
    const response = await fetch('/api/monitor', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        channel,
        recipient,
        location: 'India',
        locations,
        consent: document.getElementById('monitor-consent').checked
      })
    });
    const result = await response.json();
    if (!response.ok || result.ok !== true || !Array.isArray(result.results)) {
      throw new Error(result.error || 'Live rainfall check failed.');
    }

    const detections = result.results.filter((item) => item.detected);
    const forecastDetections = result.results.filter((item) => item.forecast_heavy_rain && !item.detected);
    const sent = result.results.filter((item) => item.alert_sent);
    const failures = result.results.filter((item) => item.error);
    const locationsChecked = Number(result.locations_checked);
    document.getElementById('live-monitor-rainfall').textContent = String(locationsChecked);
    document.getElementById('live-monitor-updated').textContent =
      `${detections.length} currently at threshold · ${forecastDetections.length} forecast crossings · Updated ${new Date().toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata', hour: '2-digit', minute: '2-digit' })} IST`;
    const resultsList = document.getElementById('live-monitor-list');
    const showResultsByDefault = resultsList.childElementCount === 0;
    resultsList.replaceChildren();
    const orderedResults = [...result.results].sort((a, b) =>
      Number(Boolean(b.detected || b.forecast_heavy_rain)) -
        Number(Boolean(a.detected || a.forecast_heavy_rain)) ||
      b.rainfall_24h - a.rainfall_24h
    );
    for (const item of orderedResults) {
      const row = document.createElement('li');
      const place = document.createElement('strong');
      const reading = document.createElement('span');
      const forecast = document.createElement('small');
      const progress = document.createElement('span');
      const progressFill = document.createElement('span');
      place.textContent = item.location;
      if (item.error) {
        reading.textContent = `ERROR · ${item.error}`;
        forecast.textContent = 'Forecast unavailable for this location.';
      } else {
        const rainArrival = item.rain_start_hours === null
          ? 'No rain forecast within 24h'
          : `Rain may start in about ${item.rain_start_hours}h${item.rain_start_time ? ` (around ${item.rain_start_time} IST)` : ''}`;
        const heavyArrival = item.heavy_rain_threshold_hours === null
          ? '64.5 mm/24h threshold not forecast within 24h'
          : `64.5 mm/24h threshold may be reached in about ${item.heavy_rain_threshold_hours}h${item.heavy_rain_threshold_time ? ` (around ${item.heavy_rain_threshold_time} IST)` : ''}${item.heavy_rain_threshold_rainfall_mm === null || item.heavy_rain_threshold_rainfall_mm === undefined ? '' : ` · projected ${item.heavy_rain_threshold_rainfall_mm} mm`}`;
        const deliveryStatus = item.alert_sent
          ? 'ALERT ACCEPTED'
          : item.already_alerted
            ? 'ALREADY ALERTED'
            : item.detected
              ? 'HEAVY RAIN NOW'
              : item.forecast_heavy_rain
                ? 'HEAVY RAIN FORECAST'
              : 'BELOW THRESHOLD';
        reading.textContent = `${Number(item.rainfall_24h).toFixed(1)} mm model-estimated in past 24h · ${deliveryStatus}`;
        forecast.textContent =
          `Next hour: ${Number(item.next_hour_rain_mm).toFixed(1)} mm · ${rainArrival} · ${heavyArrival} · Peak: ${Number(item.forecast_peak_hourly_mm).toFixed(1)} mm/h around ${item.forecast_peak_time} IST`;
        progress.className = 'monitor-threshold-progress';
        progress.setAttribute('role', 'progressbar');
        progress.setAttribute('aria-label', `${item.location} past-24-hour rainfall progress toward the ${result.threshold_mm_24h} mm heavy-rain threshold`);
        progress.setAttribute('aria-valuemin', '0');
        progress.setAttribute('aria-valuemax', String(result.threshold_mm_24h));
        progress.setAttribute('aria-valuenow', String(Math.min(Number(item.rainfall_24h), Number(result.threshold_mm_24h))));
        progressFill.style.width = `${Math.min(100, Number(item.rainfall_24h) / Number(result.threshold_mm_24h) * 100)}%`;
        progress.append(progressFill);
      }
      row.classList.toggle('heavy-rain-detected', Boolean(item.detected));
      row.classList.toggle('heavy-rain-forecast', Boolean(item.forecast_heavy_rain && !item.detected));
      if (item.error) row.classList.add('monitor-location-error');
      row.append(place, reading, forecast, progress);
      resultsList.append(row);
    }
    const resultsDisclosure = document.getElementById('live-monitor-results');
    resultsDisclosure.querySelector('summary').textContent =
      `View live readings for all ${locationsChecked} monitored cities and districts`;
    if (showResultsByDefault || detections.length > 0 || failures.length > 0) {
      resultsDisclosure.open = true;
    }

    const deliveryNote = result.delivery_configured
      ? ''
      : ` Real alerts are unavailable: ${result.delivery_setup_error || 'delivery is not configured'}`;
    status.textContent = `Monitoring all ${locationsChecked} cities and districts. ${detections.length} at/above the current 24-hour threshold; ${forecastDetections.length} forecast to reach it within 24 hours; ${sent.length} new alerts accepted${failures.length ? `; ${failures.length} delivery failures (see location readings)` : ''}.${deliveryNote}`;
    if (sent.length) {
      const placeNames = sent.map((item) => item.location).join('; ');
      showAlertNotice(`✓ ${sent.length} new heavy-rain alert${sent.length === 1 ? '' : 's'} accepted for delivery via ${channel}.\n${placeNames}`);
    }
    return true;
  } finally {
    liveMonitorCheckInProgress = false;
  }
}

async function startLiveMonitoring() {
  const form = document.getElementById('delivery-form');
  const channel = form.elements.channel.value;
  const recipient = form.elements.recipient.value.trim();
  const location = getSelectedLocation();
  const status = document.getElementById('live-monitor-status');
  if (form.elements.mode.value !== 'real') {
    status.textContent = 'Select REAL DELIVERY above before enabling automatic real alerts.';
    return;
  }
  if (!form.elements.recipient.reportValidity()) {
    document.getElementById('delivery-test').scrollIntoView({ behavior: 'smooth', block: 'center' });
    return;
  }
  if (channel !== 'Email' && !/^\+[1-9]\d{7,14}$/.test(recipient)) {
    status.textContent = 'Enter a valid international phone number above before starting monitoring.';
    return;
  }
  if (!document.getElementById('monitor-consent').checked) {
    status.textContent = 'Give explicit ongoing consent before starting automatic alerts.';
    return;
  }
  if (!location) {
    status.textContent = 'Select an Indian city or district to monitor.';
    return;
  }

  liveMonitorActive = true;
  liveMonitorDelivery = { channel, recipient };
  for (const id of ['delivery-mode', 'delivery-channel', 'delivery-recipient']) {
    document.getElementById(id).disabled = true;
  }
  document.getElementById('live-monitor').classList.add('is-monitoring');
  document.getElementById('system-status').textContent = 'LIVE MONITOR · MODEL DATA';
  document.getElementById('monitor-toggle').innerHTML = 'Stop Monitoring <span>■</span>';
  status.textContent = 'Connecting to the live weather model for the first check…';
  try {
    const checked = await checkLiveRainfall();
    if (!checked) return;
  } catch (error) {
    stopLiveMonitoring(`Live monitoring could not start: ${error.message || 'weather check failed.'}`);
    return;
  }
  liveMonitorTimer = window.setInterval(() => {
    checkLiveRainfall().catch((error) => {
      status.textContent = `Live check failed; monitoring will retry: ${error.message || 'provider error.'}`;
    });
  }, 5 * 60 * 1000);
}

document.getElementById('monitor-toggle').addEventListener('click', () => {
  if (liveMonitorActive) {
    stopLiveMonitoring();
    return;
  }
  startLiveMonitoring();
});

document.getElementById('monitor-consent').addEventListener('change', (event) => {
  if (liveMonitorActive && !event.currentTarget.checked) {
    stopLiveMonitoring('Monitoring stopped because ongoing consent was withdrawn.');
  }
});

document.getElementById('delivery-location').addEventListener('input', (event) => {
  const location = event.currentTarget.value.trim() || `${activeLocation.name}, ${activeLocation.state}`;
  document.getElementById('outgoing-preview-message').textContent =
    `Recipient location: ${location}\n${currentAlertMessage(activeLocation, currentScenario)}\nA real message is only sent in REAL DELIVERY mode after consent.`;
});

document.getElementById('delivery-location').value = `${activeLocation.name}, ${activeLocation.state}`;
document.getElementById('outgoing-preview-message').textContent = currentAlertMessage(activeLocation, currentScenario);
updateDeliveryMode();
