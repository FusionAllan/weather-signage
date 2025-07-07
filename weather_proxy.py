from flask import Flask, jsonify
from flask_cors import CORS
import requests
import time
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("OWM_API_KEY")
LAT, LON = 45.4297, -89.1534
CACHE_DURATION = 86.4  # seconds between fetches to stay under 1000/day
cached_data = None
last_fetch = 0

@app.route("/api/weather")
def get_weather():
    global cached_data, last_fetch
    now = time.time()

    if cached_data is None or (now - last_fetch) > CACHE_DURATION:
        print("⏳ Fetching fresh weather data...")
        url = (
            f"https://api.openweathermap.org/data/3.0/onecall?"
            f"lat={LAT}&lon={LON}&exclude=minutely,hourly&units=imperial&appid={API_KEY}"
        )
        try:
            response = requests.get(url)
            response.raise_for_status()
            cached_data = response.json()
            cached_data["fetched_at"] = now
            last_fetch = now
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return jsonify({"error": "Weather fetch failed"}), 500

    else:
        print("✅ Using cached weather data")

    return jsonify(cached_data)
