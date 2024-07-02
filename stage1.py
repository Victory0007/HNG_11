from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name')
    client_ip = request.remote_addr

    # location data and temperature for illustration purposes
    location = "New York"
    temperature = 11

    response = {
        "client_ip": client_ip,
        "location": location,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)