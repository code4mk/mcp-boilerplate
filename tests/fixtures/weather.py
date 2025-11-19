"""Weather-related test fixtures."""
import pytest
from datetime import datetime, timedelta


@pytest.fixture
def sample_weather_data():
    """Sample weather forecast data for testing.
    
    Returns:
        dict: A complete weather forecast dictionary with 3 days of data
              for Cox's Bazar, Bangladesh.
              
    Example:
        >>> def test_weather_parsing(sample_weather_data):
        ...     assert sample_weather_data["days"] == 3
        ...     assert len(sample_weather_data["forecast"]) == 3
    """
    today = datetime.today()
    return {
        "location": "Cox's Bazar, Bangladesh",
        "coordinates": {"latitude": 21.4272, "longitude": 92.0058},
        "start_date": today.strftime("%Y-%m-%d"),
        "end_date": (today + timedelta(days=2)).strftime("%Y-%m-%d"),
        "days": 3,
        "timezone": "Asia/Dhaka",
        "forecast": [
            {
                "day": 1,
                "date": today.strftime("%Y-%m-%d"),
                "temp_max": 30.0,
                "temp_min": 25.0,
                "temp_avg": 27.5,
                "precipitation": 0.0,
                "weather": "Clear sky",
                "weathercode": 0,
                "windspeed": 15.0,
                "sunrise": "06:00",
                "sunset": "18:00",
            },
            {
                "day": 2,
                "date": (today + timedelta(days=1)).strftime("%Y-%m-%d"),
                "temp_max": 32.0,
                "temp_min": 26.0,
                "temp_avg": 29.0,
                "precipitation": 5.0,
                "weather": "Moderate rain",
                "weathercode": 63,
                "windspeed": 20.0,
                "sunrise": "06:01",
                "sunset": "18:01",
            },
            {
                "day": 3,
                "date": (today + timedelta(days=2)).strftime("%Y-%m-%d"),
                "temp_max": 28.0,
                "temp_min": 24.0,
                "temp_avg": 26.0,
                "precipitation": 0.0,
                "weather": "Partly cloudy",
                "weathercode": 2,
                "windspeed": 12.0,
                "sunrise": "06:02",
                "sunset": "18:02",
            },
        ],
    }


@pytest.fixture
def mock_open_meteo_response():
    """Mock Open-Meteo API response.
    
    Returns:
        dict: A mock response matching the Open-Meteo API format
              with 3 days of weather data.
              
    Example:
        >>> def test_api_parsing(mock_open_meteo_response):
        ...     daily = mock_open_meteo_response["daily"]
        ...     assert len(daily["time"]) == 3
    """
    today = datetime.today()
    dates = [
        today.strftime("%Y-%m-%d"),
        (today + timedelta(days=1)).strftime("%Y-%m-%d"),
        (today + timedelta(days=2)).strftime("%Y-%m-%d"),
    ]
    return {
        "daily": {
            "time": dates,
            "temperature_2m_max": [30.0, 32.0, 28.0],
            "temperature_2m_min": [25.0, 26.0, 24.0],
            "precipitation_sum": [0.0, 5.0, 0.0],
            "weathercode": [0, 63, 2],
            "windspeed_10m_max": [15.0, 20.0, 12.0],
            "sunrise": [
                f"{dates[0]}T06:00",
                f"{dates[1]}T06:01",
                f"{dates[2]}T06:02",
            ],
            "sunset": [
                f"{dates[0]}T18:00",
                f"{dates[1]}T18:01",
                f"{dates[2]}T18:02",
            ],
        }
    }

