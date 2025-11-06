"""Weather forecast utility using Open-Meteo API."""

import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dateutil import parser


# Cox's Bazar coordinates
COX_BAZAR_LAT = 21.4272
COX_BAZAR_LON = 92.0058


def get_weather_forecast(start_date: str, days: int) -> Dict[str, Any]:
    """
    Fetch weather forecast from Open-Meteo API for Cox's Bazar.
    
    Args:
        start_date: Start date in various formats (e.g., "2025-01-15", "15 Jan 2025", "today")
        days: Number of days to fetch forecast for (1-16)
    
    Returns:
        Dictionary containing location, start_date, days, and detailed forecast
    
    Raises:
        Exception: If API request fails
    """
    # Parse start date
    try:
        if start_date.lower() == "today":
            start_dt = datetime.today()
        else:
            start_dt = parser.parse(start_date)
    except Exception:
        start_dt = datetime.today()
    
    # Calculate end date
    end_dt = start_dt + timedelta(days=days - 1)
    
    # Format dates for API (YYYY-MM-DD)
    start_date_str = start_dt.strftime("%Y-%m-%d")
    end_date_str = end_dt.strftime("%Y-%m-%d")
    
    # Build API URL
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": COX_BAZAR_LAT,
        "longitude": COX_BAZAR_LON,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode,windspeed_10m_max,sunrise,sunset",
        "timezone": "Asia/Dhaka",
        "start_date": start_date_str,
        "end_date": end_date_str
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Debug: Check if API returned an error
        if "error" in data:
            print(f"⚠️  Open-Meteo API error: {data.get('reason', 'Unknown error')}. Using fallback data.")
            return get_fallback_forecast(start_date_str, end_date_str, days)
        
        # Parse the forecast data
        daily = data.get("daily", {})
        dates = daily.get("time", [])
        temp_max = daily.get("temperature_2m_max", [])
        temp_min = daily.get("temperature_2m_min", [])
        precipitation = daily.get("precipitation_sum", [])
        weathercodes = daily.get("weathercode", [])
        windspeed = daily.get("windspeed_10m_max", [])
        sunrise = daily.get("sunrise", [])
        sunset = daily.get("sunset", [])
        
        # Build forecast list
        forecast = []
        for i in range(len(dates)):
            # Convert weather code to description
            weather_desc = get_weather_description(weathercodes[i] if i < len(weathercodes) else 0)
            
            forecast.append({
                "day": i + 1,
                "date": dates[i],
                "temp_max": round(temp_max[i], 1) if i < len(temp_max) else None,
                "temp_min": round(temp_min[i], 1) if i < len(temp_min) else None,
                "temp_avg": round((temp_max[i] + temp_min[i]) / 2, 1) if i < len(temp_max) and i < len(temp_min) else None,
                "precipitation": round(precipitation[i], 1) if i < len(precipitation) else 0,
                "weather": weather_desc,
                "weathercode": weathercodes[i] if i < len(weathercodes) else 0,
                "windspeed": round(windspeed[i], 1) if i < len(windspeed) else None,
                "sunrise": sunrise[i].split("T")[1] if i < len(sunrise) else None,
                "sunset": sunset[i].split("T")[1] if i < len(sunset) else None,
            })
        
        return {
            "location": "Cox's Bazar, Bangladesh",
            "coordinates": {"latitude": COX_BAZAR_LAT, "longitude": COX_BAZAR_LON},
            "start_date": start_date_str,
            "end_date": end_date_str,
            "days": days,
            "timezone": "Asia/Dhaka",
            "forecast": forecast
        }
        
    except Exception as e:
        # Fallback to mock data if API fails
        print(f"⚠️  Open-Meteo API error: {e}. Using fallback data.")
        return get_fallback_forecast(start_date_str, end_date_str, days)


def get_weather_description(weathercode: int) -> str:
    """
    Convert WMO weather code to human-readable description.
    
    Args:
        weathercode: WMO weather code
    
    Returns:
        Human-readable weather description
    """
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return weather_codes.get(weathercode, "Unknown")


def get_fallback_forecast(start_date: str, end_date: str, days: int) -> Dict[str, Any]:
    """
    Provide fallback forecast data when API is unavailable.
    
    Args:
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        days: Number of days
    
    Returns:
        Mock forecast data
    """
    forecast = []
    base_temp = 28
    
    # Parse start date to generate proper dates for each day
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    
    for i in range(days):
        current_date = start_dt + timedelta(days=i)
        temp_variation = (i % 3) - 1  # Creates variation: -1, 0, 1
        temp_max = base_temp + 2 + temp_variation
        temp_min = base_temp - 3 + temp_variation
        
        forecast.append({
            "day": i + 1,
            "date": current_date.strftime("%Y-%m-%d"),
            "temp_max": temp_max,
            "temp_min": temp_min,
            "temp_avg": round((temp_max + temp_min) / 2, 1),
            "precipitation": 0,
            "weather": "Partly cloudy",
            "weathercode": 2,
            "windspeed": 15.0,
            "sunrise": "06:00",
            "sunset": "18:00",
        })
    
    return {
        "location": "Cox's Bazar, Bangladesh",
        "coordinates": {"latitude": COX_BAZAR_LAT, "longitude": COX_BAZAR_LON},
        "start_date": start_date,
        "end_date": end_date,
        "days": days,
        "timezone": "Asia/Dhaka",
        "forecast": forecast,
        "note": "⚠️  Fallback data - API unavailable"
    }


def get_activity_suggestions(temperature: float, time_of_day: str = "afternoon") -> List[str]:
    """
    Suggest activities based on temperature and time of day.
    
    Args:
        temperature: Temperature in Celsius
        time_of_day: "morning", "afternoon", or "evening"
    
    Returns:
        List of suggested activities
    """
    suggestions = []
    
    if time_of_day == "morning":
        if temperature < 28:
            suggestions = [
                "Beach walk and photography",
                "Visit Himchari National Park",
                "Sunrise at Laboni Beach",
                "Morning yoga on the beach"
            ]
        else:
            suggestions = [
                "Early morning swim",
                "Sunrise boat ride",
                "Visit Inani Beach",
                "Morning market exploration"
            ]
    
    elif time_of_day == "afternoon":
        if temperature < 30:
            suggestions = [
                "Visit Aggameda Khyang monastery",
                "Explore Ramu Buddhist Village",
                "Maheshkhali Island tour",
                "Marine Drive scenic route"
            ]
        else:
            suggestions = [
                "Indoor activities - shopping at local markets",
                "Visit Bangabandhu Safari Park",
                "Relax at beach resorts",
                "Water sports activities"
            ]
    
    else:  # evening
        suggestions = [
            "Sunset at Sugandha Beach",
            "Seafood dinner at local restaurants",
            "Beach bonfire",
            "Night market shopping",
            "Cultural performances"
        ]
    
    return suggestions

