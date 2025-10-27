from flask import Flask, render_template, request
import requests
import time
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Static metric example
metrics.info('app_info', 'Application info', version='1.0.0')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    response_time = None
    error = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            # Use Open-Meteo Geocoding to get lat/lon (no key needed)
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
            try:
                geo_start = time.perf_counter()
                geo_response = requests.get(geo_url)
                geo_time = time.perf_counter() - geo_start
                if geo_response.status_code == 200:
                    geo_data = geo_response.json()
                    if 'results' in geo_data and geo_data['results']:
                        lat = geo_data['results'][0]['latitude']
                        lon = geo_data['results'][0]['longitude']
                        # Now fetch weather
                        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code&timezone=auto"
                        weather_start = time.perf_counter()
                        weather_response = requests.get(weather_url)
                        response_time = (time.perf_counter() - weather_start) + geo_time  # Total time
                        if weather_response.status_code == 200:
                            weather_data = weather_response.json()['current']
                        else:
                            error = f"Weather API error: {weather_response.status_code}"
                    else:
                        error = "City not found"
                else:
                    error = f"Geocoding error: {geo_response.status_code}"
            except Exception as e:
                error = f"Error fetching weather: {str(e)}"
    return render_template('index.html', weather_data=weather_data, response_time=response_time, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)