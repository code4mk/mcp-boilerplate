from mcp_server.mcp_instance import mcp
from mcp.server.fastmcp import Context
from datetime import datetime
from dateutil import parser
from mcp_server.components.prompts.travel_prompts import generate_itinerary_prompt, weather_based_activities_prompt
from mcp_server.utils.get_weather_forecast import get_activity_suggestions as get_suggestions
from mcp_server.components.resources.weather import resource_weather_forecast
from mcp_server.utils.elicitation import elicit_trip_extension

@mcp.tool()
async def cox_ai_itinerary(start_date: str, days: int, ctx: Context) -> str:
    """
    Full workflow: fetch daily temperatures + generate AI itinerary.
    Uses the registered MCP prompt 'generate_itinerary' for consistency.
    
    Args:
        days: Number of days for the trip
        start_date: Start date (e.g., "2025-01-15", "15 Jan 2025", "today")
    
    Returns:
        Formatted prompt for AI to generate detailed itinerary
    """
    
    # Elicit trip extension if needed (minimum 2 days recommended)
    try:
        days, elicitation_note = await elicit_trip_extension(ctx, start_date, days, min_days=2)
    except ValueError as e:
        # User cancelled the trip extension
        return str(e)
    
    # Parse start date
    try:
        start_date = parser.parse(start_date)
    except Exception:
        start_date = datetime.today()

    # Get weather forecast
    weather_data = await resource_weather_forecast(start_date, days)
    
    # Generate base itinerary prompt
    base_prompt = await generate_itinerary_prompt(days, start_date)
    
    # Generate weather-based activities prompt
    weather_prompt = await weather_based_activities_prompt(weather_data)
    
    # Format output
    output = f"""# Cox's Bazar Itinerary Planning

## Trip Details
- **Location:** {weather_data['location']}
- **Start Date:** {weather_data['start_date']}
- **Duration:** {days} day(s)
- **Timezone:** {weather_data['timezone']}

## Weather Forecast

"""
    
    # Add detailed forecast
    for day in weather_data['forecast']:
        output += f"""### Day {day['day']} - {day['date']}
- **Weather:** {day['weather']}
- **Temperature:** {day['temp_min']}°C - {day['temp_max']}°C (Average: {day['temp_avg']}°C)
- **Precipitation:** {day['precipitation']}mm
- **Wind Speed:** {day['windspeed']} km/h
- **Sunrise:** {day['sunrise']} | **Sunset:** {day['sunset']}

**Activity Suggestions:**
"""
        
        # Get activity suggestions for different times
        temp_avg = day['temp_avg']
        morning_activities = get_suggestions(temp_avg - 2, "morning")
        afternoon_activities = get_suggestions(temp_avg, "afternoon")
        evening_activities = get_suggestions(temp_avg, "evening")
        
        output += f"""
- **Morning:** {', '.join(morning_activities[:2])}
- **Afternoon:** {', '.join(afternoon_activities[:2])}
- **Evening:** {', '.join(evening_activities[:2])}

{elicitation_note}

"""
    
    output += f"""
---

## AI Itinerary Generation Prompt

{base_prompt}

---

## Weather-Based Activities Prompt

{weather_prompt}

---

**Note:** Use the above prompts with an AI assistant to generate a detailed, personalized itinerary based on the weather forecast and your preferences.
"""
    
    return output


@mcp.tool()
async def get_activity_suggestions(temperature: float, time_of_day: str = "afternoon") -> list[str]:
    """
    Suggest activities based on temperature and time of day.
    
    Args:
        temperature: Temperature in Celsius
        time_of_day: "morning", "afternoon", or "evening"
    
    Returns:
        List of suggested activities
    """
    return get_suggestions(temperature, time_of_day)
