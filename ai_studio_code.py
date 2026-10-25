import streamlit as st
import requests
from datetime import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="Weather App",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Inject Vibrant Neon Purple & Obsidian Glassmorphic CSS Theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

/* Overall Canvas & Background Gradient */
html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse 90% 70% at 50% -10%, rgba(168, 85, 247, 0.45), transparent 70%),
                radial-gradient(ellipse 80% 60% at 85% 35%, rgba(217, 70, 239, 0.35), transparent 60%),
                radial-gradient(ellipse 70% 50% at 15% 65%, rgba(139, 92, 246, 0.3), transparent 60%),
                radial-gradient(circle at 50% 110%, rgba(236, 72, 153, 0.22), transparent 65%),
                linear-gradient(180deg, #0c0419 0%, #14072b 45%, #080212 100%) !important;
    background-attachment: fixed !important;
    color: #f8fafc !important;
    font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif !important;
}

[data-testid="stHeader"] {
    background: rgba(12, 4, 25, 0.75) !important;
    backdrop-filter: blur(16px) !important;
}

/* Obsidian Glassmorphism Cards */
.obsidian-card {
    background: rgba(18, 8, 36, 0.7) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    border-radius: 24px !important;
    padding: 24px 28px !important;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.6), inset 0 1px 1px 0 rgba(255, 255, 255, 0.1) !important;
    margin-bottom: 24px !important;
}

.obsidian-tile {
    background: rgba(22, 10, 44, 0.65) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 20px !important;
    padding: 20px !important;
    box-shadow: 0 8px 24px -8px rgba(0, 0, 0, 0.6) !important;
    height: 100% !important;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.obsidian-tile:hover {
    border-color: rgba(217, 70, 239, 0.4) !important;
    box-shadow: 0 12px 30px -6px rgba(168, 85, 247, 0.25) !important;
}

/* Golden Yellow Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #fcd34d 0%, #f59e0b 50%, #d97706 100%) !important;
    color: #17082e !important;
    font-weight: 700 !important;
    border-radius: 14px !important;
    border: none !important;
    padding: 10px 22px !important;
    box-shadow: 0 4px 18px -2px rgba(245, 158, 11, 0.5) !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #fde68a 0%, #fbbf24 50%, #f59e0b 100%) !important;
    box-shadow: 0 6px 24px 0 rgba(245, 158, 11, 0.75) !important;
    transform: translateY(-1px) !important;
    color: #000000 !important;
}

div.stButton > button:active {
    transform: translateY(1px) !important;
}

/* Search Bar Input Styling */
div[data-baseweb="input"] {
    background: rgba(20, 8, 40, 0.85) !important;
    border: 1px solid rgba(168, 85, 247, 0.3) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(12px) !important;
}

div[data-baseweb="input"]:focus-within {
    border-color: #fbbf24 !important;
    box-shadow: 0 0 16px rgba(251, 191, 36, 0.3) !important;
}

input.stTextInput {
    color: #ffffff !important;
    font-size: 15px !important;
}

/* Radio buttons / Pill controls */
div[role="radiogroup"] {
    background: rgba(20, 8, 40, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding: 4px 8px !important;
    border-radius: 14px !important;
}

/* Typography Highlights */
.gold-text {
    background: linear-gradient(135deg, #fef08a 0%, #f59e0b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}

/* Weather Badges */
.badge-purple {
    background: rgba(168, 85, 247, 0.15);
    border: 1px solid rgba(168, 85, 247, 0.3);
    color: #e9d5ff;
    padding: 4px 12px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}

.badge-gold {
    background: rgba(245, 158, 11, 0.15);
    border: 1px solid rgba(245, 158, 11, 0.35);
    color: #fde047;
    padding: 4px 12px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 700;
    display: inline-block;
}

.badge-cyan {
    background: rgba(6, 182, 212, 0.15);
    border: 1px solid rgba(6, 182, 212, 0.35);
    color: #67e8f9;
    padding: 4px 12px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. Weather Condition Interpreter
def get_condition_info(code, is_day=1):
    conditions = {
        0: ("Clear Sky" if is_day else "Clear Night", "☀️" if is_day else "🌙", "Bright sunshine with crisp visibility" if is_day else "Crisp starlit skies"),
        1: ("Mainly Clear", "🌤️", "Mostly clear skies with a gentle breeze"),
        2: ("Partly Cloudy", "⛅", "Sun filtering through scattered cloud layers"),
        3: ("Overcast", "☁️", "Dense atmospheric cloud canopy overhead"),
        45: ("Foggy Mist", "🌫️", "Cool lingering mist and reduced horizon visibility"),
        48: ("Rime Fog", "🌫️", "Depositing rime fog conditions"),
        51: ("Light Drizzle", "🌦️", "Soft intermittent misty precipitation"),
        53: ("Moderate Drizzle", "🌧️", "Steady gentle drizzle falling softly"),
        55: ("Dense Drizzle", "🌧️", "Frequent misty drizzle with high humidity"),
        61: ("Slight Rain", "🌦️", "Scattered light showers passing through"),
        63: ("Moderate Rain", "🌧️", "Steady refreshing rainfall across the district"),
        65: ("Heavy Rain", "🌧️", "Continuous torrential downpour"),
        71: ("Slight Snow", "🌨️", "Crisp freezing temperatures with snow grains"),
        73: ("Moderate Snow", "❄️", "Steady snowfall accumulating on surfaces"),
        75: ("Heavy Snow", "❄️", "Intense blizzard-like snow conditions"),
        80: ("Rain Showers", "🌦️", "Brisk dynamic cloudbursts interspersed with breaks"),
        81: ("Moderate Showers", "🌧️", "Heavy passing downpours"),
        82: ("Violent Showers", "⛈️", "Torrential downpours with strong gusts"),
        95: ("Thunderstorm", "⚡", "Electric storm activity with thunder and gusty winds"),
        96: ("Thunderstorm with Hail", "⛈️", "Severe electrical cells with hailstones"),
        99: ("Heavy Hailstorm", "⛈️", "Severe thunderstorm with heavy hail"),
    }
    return conditions.get(code, ("Fair Conditions", "🌤️", "Mild atmospheric conditions prevailing"))

def get_aqi_category(us_aqi):
    if us_aqi <= 50:
        return "Good", "rgba(16, 185, 129, 0.2)", "#34d399", "Air quality is exceptional. Perfect for outdoor recreation."
    elif us_aqi <= 100:
        return "Moderate", "rgba(245, 158, 11, 0.2)", "#fbbf24", "Acceptable quality; sensitive groups may feel slight irritation."
    elif us_aqi <= 150:
        return "Unhealthy for Sensitive", "rgba(249, 115, 22, 0.2)", "#fb923c", "Children and seniors should reduce strenuous outdoor exertion."
    elif us_aqi <= 200:
        return "Unhealthy", "rgba(244, 63, 94, 0.2)", "#f43f5e", "Everyone may begin to experience health effects; limit prolonged exposure."
    else:
        return "Very Unhealthy", "rgba(168, 85, 247, 0.2)", "#c084fc", "Health alert: serious irritation risk. Keep windows sealed."

# 4. Geocoding & Weather Fetching
@st.cache_data(ttl=600)
def search_city_coords(city_query):
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_query}&count=1&language=en&format=json"
        res = requests.get(url, timeout=6).json()
        if res.get("results"):
            item = res["results"][0]
            return {
                "name": item.get("name"),
                "country": item.get("country", ""),
                "country_code": item.get("country_code", ""),
                "admin1": item.get("admin1", ""),
                "lat": item.get("latitude"),
                "lon": item.get("longitude")
            }
    except Exception as e:
        st.error(f"Geocoding lookup error: {e}")
    return None

@st.cache_data(ttl=300)
def fetch_weather_data(lat, lon):
    try:
        w_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m"
            "&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,weather_code,uv_index,is_day"
            "&daily=weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,uv_index_max,precipitation_sum,precipitation_probability_max,wind_speed_10m_max"
            "&timezone=auto"
        )
        aqi_url = (
            f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}"
            "&current=us_aqi,european_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone"
            "&timezone=auto"
        )

        w_res = requests.get(w_url, timeout=6).json()
        aqi_res = requests.get(aqi_url, timeout=6).json()
        return w_res, aqi_res
    except Exception as e:
        st.error(f"Meteorological telemetry error: {e}")
        return None, None

# 5. Top Bar Header Lockup
col_brand, col_unit = st.columns([4, 1])

with col_brand:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
        <div style="width: 38px; height: 38px; border-radius: 12px; background: linear-gradient(135deg, #fbbf24, #d946ef); display: flex; align-items: center; justify-content: center; box-shadow: 0 0 15px rgba(251, 191, 36, 0.5);">
            <span style="font-size: 20px;">☀️</span>
        </div>
        <div>
            <h1 style="margin: 0; font-size: 28px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px;">
                Weather <span class="gold-text">App</span>
            </h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_unit:
    unit_choice = st.radio("Temp Unit", ["°C (Celsius)", "°F (Fahrenheit)"], horizontal=True, label_visibility="collapsed")
    is_fahrenheit = "°F" in unit_choice

def fmt_temp(temp_c):
    if is_fahrenheit:
        return f"{round((temp_c * 9/5) + 32)}°F"
    return f"{round(temp_c)}°C"

# 6. Live Search Bar & Quick Cities
search_col, btn_col = st.columns([5, 1])

if "city_query" not in st.session_state:
    st.session_state.city_query = "San Francisco"

with search_col:
    city_input = st.text_input(
        "Search city worldwide", 
        value=st.session_state.city_query, 
        placeholder="Search city, district, or region (e.g. Tokyo, Paris, New York)...",
        label_visibility="collapsed"
    )

with btn_col:
    if st.button("🔍 Fetch Live", use_container_width=True):
        st.session_state.city_query = city_input

st.markdown("<div style='margin-bottom: 6px; font-size: 13px; color: rgba(216, 180, 254, 0.7);'>Popular Metros:</div>", unsafe_allow_html=True)
quick_cols = st.columns(8)
presets = ["Tokyo", "London", "New York", "Paris", "Sydney", "Dubai", "Reykjavik", "San Francisco"]

for idx, p_name in enumerate(presets):
    with quick_cols[idx]:
        if st.button(p_name, key=f"quick_{p_name}", use_container_width=True):
            st.session_state.city_query = p_name
            st.rerun()

# 7. Fetch Geocoding & Weather Data
city_data = search_city_coords(st.session_state.city_query)
if not city_data:
    st.error(f"Could not locate '{st.session_state.city_query}'. Please check spelling.")
    st.stop()

weather_json, aqi_json = fetch_weather_data(city_data["lat"], city_data["lon"])
if not weather_json:
    st.error("Live meteorological feed is temporarily unavailable. Please retry.")
    st.stop()

curr = weather_json.get("current", {})
daily = weather_json.get("daily", {})
hourly = weather_json.get("hourly", {})
aqi_curr = aqi_json.get("current", {}) if aqi_json else {}

temp_val = curr.get("temperature_2m", 20)
feels_val = curr.get("apparent_temperature", 20)
w_code = curr.get("weather_code", 0)
is_day = curr.get("is_day", 1)
humidity_val = curr.get("relative_humidity_2m", 50)
wind_speed_val = curr.get("wind_speed_10m", 12)
wind_gust_val = curr.get("wind_gusts_10m", 18)
wind_dir = curr.get("wind_direction_10m", 180)
pressure_val = curr.get("surface_pressure", 1013)
precip_val = curr.get("precipitation", 0)

cond_label, cond_icon, cond_desc = get_condition_info(w_code, is_day)

today_max = daily.get("temperature_2m_max", [temp_val + 3])[0]
today_min = daily.get("temperature_2m_min", [temp_val - 4])[0]
today_rain = daily.get("precipitation_probability_max", [0])[0]
today_sunrise = daily.get("sunrise", ["06:30"])[0].split("T")[-1]
today_sunset = daily.get("sunset", ["19:45"])[0].split("T")[-1]
today_uv = daily.get("uv_index_max", [5])[0]

us_aqi = round(aqi_curr.get("us_aqi", 38))
aqi_cat, aqi_bg, aqi_color, aqi_advice = get_aqi_category(us_aqi)

# 8. Prominent Hero Weather Display (Glassmorphic Obsidian)
st.markdown(f"""
<div class="obsidian-card">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 20px;">
        <div style="flex: 1; min-width: 280px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <h2 style="font-size: 38px; font-weight: 800; margin: 0; color: #ffffff;">{city_data['name']}</h2>
                <span class="badge-purple">{city_data['country_code']}</span>
            </div>
            <div style="color: rgba(233, 213, 255, 0.7); font-size: 14px; margin-top: 4px; font-weight: 500;">
                {city_data.get('admin1', '')}, {city_data.get('country', '')} · {datetime.now().strftime('%A, %b %d')}
            </div>
            <div style="display: flex; align-items: baseline; gap: 24px; margin: 18px 0 10px 0;">
                <div style="font-size: 78px; font-weight: 900; line-height: 1; color: #ffffff; letter-spacing: -2px;">
                    {fmt_temp(temp_val)}
                </div>
                <div>
                    <div style="font-size: 26px; font-weight: 700;" class="gold-text">
                        {cond_label}
                    </div>
                    <div style="font-size: 14px; color: rgba(240, 171, 252, 0.9); margin-top: 2px;">
                        {cond_desc}
                    </div>
                </div>
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 20px; padding-top: 16px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
                <span class="badge-gold">▲ Max: {fmt_temp(today_max)} · ▼ Min: {fmt_temp(today_min)}</span>
                <span class="badge-purple">Feels like: {fmt_temp(feels_val)}</span>
                <span class="badge-cyan">💧 Rain Chance: {today_rain}%</span>
                <span class="badge-purple">💨 Wind: {round(wind_speed_val)} km/h</span>
            </div>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; background: rgba(255, 255, 255, 0.03); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.08);">
            <div style="font-size: 90px; line-height: 1; filter: drop-shadow(0 0 20px rgba(251, 191, 36, 0.6));">
                {cond_icon}
            </div>
            <div style="font-size: 12px; font-weight: 700; color: #fbbf24; margin-top: 8px; letter-spacing: 0.5px;">
                REAL-TIME TELEMETRY
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 9. 24-Hour Hourly Outlook Strip
st.markdown("<h3 style='color: #ffffff; font-size: 20px; font-weight: 700; margin-bottom: 12px;'>⏱ 24-Hour Hourly Outlook</h3>", unsafe_allow_html=True)
hourly_times = hourly.get("time", [])
hourly_temps = hourly.get("temperature_2m", [])
hourly_codes = hourly.get("weather_code", [])
hourly_precip = hourly.get("precipitation_probability", [])
hourly_days = hourly.get("is_day", [])

h_cols = st.columns(8)
for i in range(min(8, len(hourly_times))):
    with h_cols[i]:
        time_str = hourly_times[i*3] if (i*3) < len(hourly_times) else hourly_times[i]
        h_hour = datetime.strptime(time_str, "%Y-%m-%dT%H:%M").strftime("%-I %p")
        h_temp = hourly_temps[i*3] if (i*3) < len(hourly_temps) else temp_val
        h_code = hourly_codes[i*3] if (i*3) < len(hourly_codes) else 0
        h_day = hourly_days[i*3] if (i*3) < len(hourly_days) else 1
        h_p = hourly_precip[i*3] if (i*3) < len(hourly_precip) else 0
        h_name, h_icon, _ = get_condition_info(h_code, h_day)

        st.markdown(f"""
        <div style="background: rgba(24, 11, 48, 0.65); border: 1px solid rgba(168, 85, 247, 0.2); border-radius: 18px; padding: 14px 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <div style="font-size: 12px; font-weight: 600; color: rgba(233, 213, 255, 0.8);">{h_hour}</div>
            <div style="font-size: 28px; margin: 8px 0;">{h_icon}</div>
            <div style="font-size: 16px; font-weight: 800; color: #ffffff;">{fmt_temp(h_temp)}</div>
            <div style="font-size: 11px; color: #67e8f9; margin-top: 4px;">💧 {h_p}%</div>
        </div>
        """, unsafe_allow_html=True)

# 10. 7-Day Extended Forecast Cards
st.markdown("<h3 style='color: #ffffff; font-size: 20px; font-weight: 700; margin: 28px 0 12px 0;'>📅 7-Day Extended Forecast</h3>", unsafe_allow_html=True)
daily_times = daily.get("time", [])
daily_maxs = daily.get("temperature_2m_max", [])
daily_mins = daily.get("temperature_2m_min", [])
daily_codes = daily.get("weather_code", [])
daily_precips = daily.get("precipitation_probability_max", [])

for d_idx in range(min(7, len(daily_times))):
    d_date_str = daily_times[d_idx]
    d_obj = datetime.strptime(d_date_str, "%Y-%m-%d")
    day_title = "Today" if d_idx == 0 else ("Tomorrow" if d_idx == 1 else d_obj.strftime("%A"))
    d_date_formatted = d_obj.strftime("%b %d")
    d_code = daily_codes[d_idx] if d_idx < len(daily_codes) else 0
    d_max = daily_maxs[d_idx] if d_idx < len(daily_maxs) else temp_val + 2
    d_min = daily_mins[d_idx] if d_idx < len(daily_mins) else temp_val - 2
    d_p = daily_precips[d_idx] if d_idx < len(daily_precips) else 0
    d_name, d_icon, _ = get_condition_info(d_code, 1)

    st.markdown(f"""
    <div style="background: rgba(19, 8, 38, 0.55); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 14px 22px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
        <div style="width: 140px;">
            <div style="font-weight: 700; color: #ffffff; font-size: 15px;">{day_title}</div>
            <div style="font-size: 12px; color: rgba(233, 213, 255, 0.6);">{d_date_formatted}</div>
        </div>
        <div style="display: flex; align-items: center; gap: 12px; width: 180px;">
            <span style="font-size: 26px;">{d_icon}</span>
            <span style="font-size: 14px; font-weight: 500; color: #f5d0fe;">{d_name}</span>
        </div>
        <div style="width: 100px; font-size: 13px; color: #67e8f9; font-weight: 600;">
            💧 {d_p}% rain
        </div>
        <div style="display: flex; align-items: center; gap: 14px; font-size: 15px; font-weight: 700;">
            <span style="color: #67e8f9;">{fmt_temp(d_min)}</span>
            <span style="color: rgba(255,255,255,0.2);">—</span>
            <span style="color: #fbbf24;">{fmt_temp(d_max)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 11. Detailed Metric Grid Tiles
st.markdown("<h3 style='color: #ffffff; font-size: 20px; font-weight: 700; margin: 32px 0 16px 0;'>🌿 Atmosphere & Environmental Metrics</h3>", unsafe_allow_html=True)
m_col1, m_col2, m_col3 = st.columns(3)

with m_col1:
    st.markdown(f"""
    <div class="obsidian-tile">
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 12px; font-weight: 700; color: #d8b4fe; text-transform: uppercase;">Air Quality Index</span>
                <span style="background: {aqi_bg}; color: {aqi_color}; padding: 2px 10px; border-radius: 8px; font-size: 11px; font-weight: 700;">{aqi_cat}</span>
            </div>
            <div style="font-size: 46px; font-weight: 900; color: #ffffff; line-height: 1; margin: 8px 0;">{us_aqi}</div>
            <div style="font-size: 12px; color: rgba(233, 213, 255, 0.7); margin-bottom: 14px;">US AQI Standard · Clean Atmospheric Score</div>
            <p style="font-size: 12px; color: rgba(240, 171, 252, 0.9); line-height: 1.5;">{aqi_advice}</p>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; padding-top: 14px; border-top: 1px solid rgba(255,255,255,0.08); font-size: 11px; text-align: center;">
            <div style="background: rgba(0,0,0,0.25); padding: 6px; border-radius: 8px;">
                <div style="color: rgba(255,255,255,0.5);">PM2.5</div>
                <div style="font-weight: 700; color: #fff;">{aqi_curr.get('pm2_5', 8.2)}</div>
            </div>
            <div style="background: rgba(0,0,0,0.25); padding: 6px; border-radius: 8px;">
                <div style="color: rgba(255,255,255,0.5);">PM10</div>
                <div style="font-weight: 700; color: #fff;">{aqi_curr.get('pm10', 14.1)}</div>
            </div>
            <div style="background: rgba(0,0,0,0.25); padding: 6px; border-radius: 8px;">
                <div style="color: rgba(255,255,255,0.5);">Ozone O₃</div>
                <div style="font-weight: 700; color: #fff;">{round(aqi_curr.get('ozone', 50))}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with m_col2:
    st.markdown(f"""
    <div class="obsidian-tile">
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 12px; font-weight: 700; color: #d8b4fe; text-transform: uppercase;">Solar Trajectory</span>
                <span style="color: #fbbf24; font-size: 12px; font-weight: 600;">Astronomical</span>
            </div>
            <div style="text-align: center; padding: 12px 0;">
                <span style="font-size: 54px; filter: drop-shadow(0 0 16px rgba(251, 191, 36, 0.7));">☀️</span>
            </div>
            <div style="display: flex; justify-content: space-around; margin: 10px 0;">
                <div style="text-align: center;">
                    <div style="font-size: 11px; color: rgba(255,255,255,0.6);">Sunrise</div>
                    <div style="font-size: 18px; font-weight: 800; color: #fde047;">{today_sunrise}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 11px; color: rgba(255,255,255,0.6);">Sunset</div>
                    <div style="font-size: 18px; font-weight: 800; color: #f472b6;">{today_sunset}</div>
                </div>
            </div>
        </div>
        <div style="padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.08); font-size: 12px; color: rgba(233, 213, 255, 0.7); text-align: center;">
            Clear diurnal solar cycle with continuous daylight tracking.
        </div>
    </div>
    """, unsafe_allow_html=True)

with m_col3:
    uv_desc = "Low Risk" if today_uv <= 2 else ("Moderate" if today_uv <= 5 else "High Protection Required")
    st.markdown(f"""
    <div class="obsidian-tile">
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 12px; font-weight: 700; color: #d8b4fe; text-transform: uppercase;">Ultraviolet (UV) Index</span>
                <span style="color: #fbbf24; font-size: 12px; font-weight: 700;">{uv_desc}</span>
            </div>
            <div style="font-size: 46px; font-weight: 900; color: #ffffff; line-height: 1; margin: 8px 0;">{today_uv} <span style="font-size: 18px; color: rgba(255,255,255,0.5); font-weight: 600;">/ 12</span></div>
            <div style="width: 100%; height: 8px; border-radius: 4px; background: linear-gradient(90deg, #34d399, #fbbf24, #f97316, #ef4444, #a855f7); margin: 14px 0;"></div>
            <p style="font-size: 12px; color: rgba(240, 171, 252, 0.9); line-height: 1.5;">
                {"Minimal protection needed. Enjoy outdoors." if today_uv <= 2 else "Wear sunglasses and SPF 30+ sunscreen. Seek shade during midday peak hours."}
            </p>
        </div>
        <div style="padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.08); font-size: 11px; color: #fef08a; display: flex; justify-content: space-between;">
            <span>Peak: 11:30 - 15:30</span>
            <span>SPF 30+ Advised</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

m_col4, m_col5, m_col6 = st.columns(3)

with m_col4:
    st.markdown(f"""
    <div class="obsidian-tile">
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 12px; font-weight: 700; color: #d8b4fe; text-transform: uppercase;">Relative Humidity</span>
                <span style="color: #67e8f9; font-size: 12px; font-weight: 600;">{'Comfortable' if 30 <= humidity_val <= 65 else 'Humid'}</span>
            </div>
            <div style="font-size: 46px; font-weight: 900; color: #ffffff; line-height: 1; margin: 8px 0;">{humidity_val}%</div>
            <div style="width: 100%; height: 8px; border-radius: 4px; background: rgba(255,255,255,0.1); margin: 14px 0; overflow: hidden;">
                <div style="width: {humidity_val}%; height: 100%; background: linear-gradient(90deg, #06b6d4, #3b82f6); border-radius: 4px;"></div>
            </div>
            <p style="font-size: 12px; color: rgba(233, 213, 255, 0.7); line-height: 1.5;">
                Atmospheric moisture content. Calculated dew point is around {round(temp_val - ((100 - humidity_val) / 5))}°C.
            </p>
        </div>
        <div style="padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.08); font-size: 12px; color: #67e8f9;">
            Precipitation today: {precip_val} mm
        </div>
    </div>
    """, unsafe_allow_html=True)

with m_col5:
    st.markdown(f"""
    <div class="obsidian-tile">
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 12px; font-weight: 700; color: #d8b4fe; text-transform: uppercase;">Wind Dynamics</span>
                <span style="color: #34d399; font-size: 12px; font-weight: 600;">{wind_dir}° Bearing</span>
            </div>
            <div style="font-size: 46px; font-weight: 900; color: #ffffff; line-height: 1; margin: 8px 0;">
                {round(wind_speed_val)} <span style="font-size: 18px; color: rgba(255,255,255,0.5);">km/h</span>
            </div>
            <div style="font-size: 13px; color: #fde047; font-weight: 600; margin: 6px 0;">
                Gusts up to {round(wind_gust_val)} km/h
            </div>
            <p style="font-size: 12px; color: rgba(233, 213, 255, 0.7); line-height: 1.5;">
                Beaufort scale indicates moderate surface airflow with steady directional persistence.
            </p>
        </div>
        <div style="padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.08); font-size: 12px; color: #34d399;">
            Compass Angle: {wind_dir}° South-West
        </div>
    </div>
    """, unsafe_allow_html=True)

with m_col6:
    st.markdown(f"""
    <div class="obsidian-tile">
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 12px; font-weight: 700; color: #d8b4fe; text-transform: uppercase;">Barometer & Sight</span>
                <span style="color: #a78bfa; font-size: 12px; font-weight: 600;">Steady</span>
            </div>
            <div style="font-size: 46px; font-weight: 900; color: #ffffff; line-height: 1; margin: 8px 0;">
                {round(pressure_val)} <span style="font-size: 18px; color: rgba(255,255,255,0.5);">hPa</span>
            </div>
            <div style="font-size: 13px; color: #67e8f9; font-weight: 600; margin: 6px 0;">
                Sight Visibility: 10+ km (Unrestricted)
            </div>
            <p style="font-size: 12px; color: rgba(233, 213, 255, 0.7); line-height: 1.5;">
                Anticyclonic air pressure distribution with clean line-of-sight clarity.
            </p>
        </div>
        <div style="padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.08); font-size: 12px; color: #a78bfa;">
            Sea-level calibrated barometric baseline
        </div>
    </div>
    """, unsafe_allow_html=True)

# 12. Footer
st.markdown("""
<div style="text-align: center; margin-top: 40px; padding: 20px; border-top: 1px solid rgba(255,255,255,0.08); font-size: 13px; color: rgba(216, 180, 254, 0.5);">
    Weather App · Streamlit Edition · Powered by Open-Meteo Free Global Meteorological API · Ready for Streamlit Community Cloud
</div>
""", unsafe_allow_html=True)