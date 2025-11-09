from typing import Dict, Any

async def get_itinerary_prompt(days: int, start_date: str) -> str:
    """
    Full workflow: fetch daily temperatures + generate AI itinerary.
    Uses the registered MCP prompt 'generate_itinerary' for consistency.
    
    Args:
        days: Number of days for the trip
        start_date: Start date (e.g., "2025-01-15", "15 Jan 2025", "today")
    
    Returns:
        Formatted prompt for AI to generate detailed itinerary
    """
    return f"""Generate a detailed {days}-day itinerary for Cox's Bazar, Bangladesh starting from {start_date}.

Consider the following in your itinerary:

1. **Daily Schedule:**
   - Morning activities (6:00 AM - 12:00 PM)
   - Afternoon activities (12:00 PM - 6:00 PM)
   - Evening activities (6:00 PM onwards)

2. **Weather-Based Recommendations:**
   - Suggest indoor activities for hot afternoons (>32°C)
   - Recommend beach activities for pleasant weather (25-30°C)
   - Include sunrise/sunset timings for beach visits

3. **Must-Visit Places:**
   - Laboni Beach (main beach, shopping, restaurants)
   - Inani Beach (pristine, less crowded)
   - Himchari National Park (waterfalls, nature trails)
   - Marine Drive (scenic coastal road)
   - Aggameda Khyang (Buddhist monastery)
   - Ramu Buddhist Village (cultural experience)
   - Maheshkhali Island (day trip)
   - Sugandha Beach (sunset views)
   - Bangabandhu Safari Park (wildlife)

4. **Activities:**
   - Beach walks and photography
   - Water sports (surfing, parasailing, jet skiing)
   - Boat rides and island hopping
   - Seafood dining experiences
   - Local market exploration
   - Cultural site visits
   - Sunrise/sunset viewing

5. **Practical Tips:**
   - Best times to visit each location
   - Transportation suggestions
   - Local cuisine recommendations
   - Safety considerations
   - Budget estimates

Please create a day-by-day itinerary with specific timings, activities, and practical tips."""


async def get_weather_based_activities_prompt(weather_data: Dict[str, Any]) -> str:
    """
    Generate activity suggestions based on weather forecast.
    
    Args:
        weather_data: Weather forecast data
    
    Returns:
        Formatted prompt with weather-based activity suggestions
    """
    forecast = weather_data.get("forecast", [])
    
    location = weather_data.get('location', 'Cox\'s Bazar')
    days = weather_data.get('days', 0)
    start_date = weather_data.get('start_date', 'N/A')
    
    prompt = f"""Based on the weather forecast for Cox's Bazar, suggest optimal activities for each day:

Location: {location}
Trip Duration: {days} days
Start Date: {start_date}

Daily Weather Summary:
"""
    
    for day in forecast:
        day_num = day.get('day', 0)
        date = day.get('date', 'N/A')
        weather = day.get('weather', 'N/A')
        temp_min = day.get('temp_min', 0)
        temp_max = day.get('temp_max', 0)
        temp_avg = day.get('temp_avg', 0)
        precipitation = day.get('precipitation', 0)
        windspeed = day.get('windspeed', 0)
        sunrise = day.get('sunrise', 'N/A')
        sunset = day.get('sunset', 'N/A')
        
        prompt += f"\nDay {day_num} ({date}):\n"
        prompt += f"- Weather: {weather}\n"
        prompt += f"- Temperature: {temp_min}°C - {temp_max}°C (Avg: {temp_avg}°C)\n"
        prompt += f"- Precipitation: {precipitation}mm\n"
        prompt += f"- Wind Speed: {windspeed} km/h\n"
        prompt += f"- Sunrise: {sunrise} | Sunset: {sunset}\n"
    
    prompt += """
Based on this weather forecast, please provide:
1. Best activities for each day considering the weather conditions
2. Time-specific recommendations (morning/afternoon/evening)
3. Indoor alternatives for rainy or very hot days
4. Optimal times for beach activities
5. Photography opportunities (sunrise/sunset)
6. Dining suggestions based on weather
"""
    
    return prompt