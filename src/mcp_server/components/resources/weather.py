from mcp_server.mcp_instance import mcp
from mcp_server.utils.get_weather_forecast import get_weather_forecast

@mcp.resource("weather://coxsbazar/forecast/{start_date}/{days}")
async def resource_weather_forecast(start_date: str, days: int):
    """
    Get weather forecast for Cox's Bazar.
    
    Args:
        start_date: Start date (e.g., "2025-01-15", "today")
        days: Number of days (1-16)
    
    Returns:
        Weather forecast data from Open-Meteo API
    """
    return get_weather_forecast(start_date, days)



