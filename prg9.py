from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = '4d7aae5a5619e6dc015e7c5645e79ca0'

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', 'London')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'

    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({
            "error": "Failed to fetch weather data",
            "details": response.json()
        }), response.status_code

    data = response.json()
    formatted = {
        "city": data['name'],
        "temperature": data['main']['temp'],
        "feels_like": data['main']['feels_like'],
        "humidity": data['main']['humidity'],
        "description": data['weather'][0]['description'],
        "wind_speed": data['wind']['speed']
    }
    return jsonify(formatted)

if __name__ == '__main__':
    app.run(debug=True, port=5000)


