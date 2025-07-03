from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # ✅ Allow all origins by default

# Coordinates for Elcho, WI
LAT = '45.4297'
LON = '-89.1534'

@app.route('/api/weather')
def get_weather():
    # Load OWM API key from environment or fallback to default if testing locally
    api_key = os.getenv('OWM_API_KEY')

    # Fetch weather data from OpenWeatherMap
    owm_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={LAT}&lon={LON}&units=imperial&appid={api_key}'
    owm_response = requests.get(owm_url)
    if owm_response.status_code != 200:
        return jsonify({'error': 'Failed to fetch weather data'}), 500
    owm_data = owm_response.json()

    # Fetch alerts from NWS
    nws_url = f'https://api.weather.gov/alerts/active?point={LAT},{LON}'
    nws_headers = {'User-Agent': 'PaperPeopleWeatherDisplay (allan@paperpeopleusa.com)'}
    nws_response = requests.get(nws_url, headers=nws_headers)
    if nws_response.status_code == 200:
        alerts = nws_response.json().get('features', [])
        formatted_alerts = []
        for alert in alerts:
            props = alert.get('properties', {})
            formatted_alerts.append({
                'event': props.get('event'),
                'description': props.get('description'),
                'severity': props.get('severity')
            })
        owm_data['alerts'] = formatted_alerts
    else:
        owm_data['alerts'] = []

    return jsonify(owm_data)
