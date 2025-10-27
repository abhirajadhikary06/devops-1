import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
import responses

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@responses.activate
def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Fetch Weather' in response.data

@responses.activate
def test_index_post_success(client):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search?name=Berlin&count=1&language=en&format=json"
    geo_mock_data = {"results": [{"latitude": 52.52, "longitude": 13.41}]}
    responses.add(responses.GET, geo_url, json=geo_mock_data, status=200)
    
    weather_url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,relative_humidity_2m,weather_code&timezone=auto"
    weather_mock_data = {"current": {"temperature_2m": 15.0, "relative_humidity_2m": 80, "weather_code": 0}}
    responses.add(responses.GET, weather_url, json=weather_mock_data, status=200)
    
    response = client.post('/', data={'city': 'Berlin'})
    assert response.status_code == 200
    assert b'Temperature: 15.0' in response.data
    assert b'Response Time:' in response.data

@responses.activate
def test_index_post_error(client):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search?name=Invalid&count=1&language=en&format=json"
    responses.add(responses.GET, geo_url, status=404)
    
    response = client.post('/', data={'city': 'Invalid'})
    assert response.status_code == 200
    assert b'Geocoding error: 404' in response.data