from flask import Flask, request, jsonify
from dotenv import find_dotenv, load_dotenv
import os
import requests

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
weather_app_api_key = os.getenv("WEATHER_APP_API_KEY")
ipregistry_api_key = os.getenv("IPREGISTRY_API_KEY")

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return "<h1> Home Page </h1>"

# @app.route('/api/hello', methods=['GET'])
# def hello():
#     visitor_name = request.args.get('visitor_name')
#     client_ip = request.remote_addr
#
#     # location data and temperature for illustration purposes
#     location = "New York"
#     temperature = 11
#
#     response = {
#         "client_ip": client_ip,
#         "location": location,
#         "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"
#     }
#
#     return jsonify(response)

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name')
    client_ip = request.remote_addr

    # Get location based on IP
    ipregistry_url = f'https://api.ipregistry.co/{client_ip}?key={ipregistry_api_key}'
    location_response = requests.get(ipregistry_url)
    location_data = location_response.json()
    city = location_data.get('location', {}).get('city', 'Unknown Location')

    # Get temperature based on location (dummy API key)
    weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={weather_app_api_key}')
    weather_data = weather_response.json()
    temperature = weather_data['main']['temp']

    # Build response
    response = {
        "client_ip": client_ip,
        "location": city,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)