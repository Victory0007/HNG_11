from flask import Flask, request, jsonify
from dotenv import find_dotenv, load_dotenv
import os
import requests
from collections import OrderedDict

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
weather_app_api_key = os.getenv("WEATHER_APP_API_KEY")
ipregistry_api_key = os.getenv("IPREGISTRY_API_KEY")

app = Flask(__name__)
app.json.sort_keys = False

@app.route("/", methods=['GET'])
def home():
    return "<h1> Home Page </h1>"

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Guest')
    client_ip = request.remote_addr

    # local testing
    if client_ip == '127.0.0.1':
        client_ip = '8.8.8.8'  # Google's public DNS for testing

    # location based on IP
    ipregistry_url = f'https://api.ipregistry.co/{client_ip}?key={ipregistry_api_key}'
    location_response = requests.get(ipregistry_url)
    if location_response.status_code != 200:
        return jsonify({"error": "Failed to retrieve location data"}), 500
    location_data = location_response.json()
    city = location_data.get('location', {}).get('city', 'Unknown Location')

    # temperature based on location
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={weather_app_api_key}'
    weather_response = requests.get(weather_url)
    if weather_response.status_code != 200:
        return jsonify({"error": "Failed to retrieve weather data"}), 500
    weather_data = weather_response.json()
    temperature = weather_data.get('main', {}).get('temp', 'N/A')

    response = OrderedDict([
        ("client_ip", client_ip),
        ("location", city),
        ("greeting", f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}")
    ])

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)