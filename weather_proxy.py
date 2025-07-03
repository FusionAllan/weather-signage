from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

# Load your secret API key securely via environment variable
API_KEY = os.environ.get("OWM_API_KEY")  # Set this in your host environment
LAT = 45.43
LON = -89.15
EXCLUDE = "minutely,hourly"
UNITS = "imperial"

@app.route("/api/weather")
def weather():
    try:
        url = (
            f"https://api.openweathermap.org/data/3.0/onecall"
            f"?lat={LAT}&lon={LON}&units={UNITS}&exclude={EXCLUDE}&appid={API_KEY}"
        )
        res = requests.get(url)
        res.raise_for_status()
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return "Weather Proxy is running"

if __name__ == "__main__":
    app.run(debug=True)