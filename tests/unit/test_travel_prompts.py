"""Unit tests for travel prompt generation."""
import pytest
from mcp_server.core.prompts.travel import (
    get_itinerary_prompt,
    get_weather_based_activities_prompt,
)


@pytest.mark.unit
class TestGetItineraryPrompt:
    """Test itinerary prompt generation and content."""
    
    @pytest.mark.asyncio
    async def test_itinerary_prompt_structure(self):
        """Test that itinerary prompt has correct basic structure."""
        prompt = await get_itinerary_prompt(3, "2025-01-15")
        
        assert isinstance(prompt, str)
        assert "3-day itinerary" in prompt.lower() or "3 day" in prompt.lower()
        assert "2025-01-15" in prompt or "Cox's Bazar" in prompt
    
    @pytest.mark.asyncio
    async def test_itinerary_prompt_includes_sections(self):
        """Test that prompt includes all key sections."""
        prompt = await get_itinerary_prompt(5, "2025-01-15")
        
        assert "Daily Schedule" in prompt or "schedule" in prompt.lower()
        assert "Weather-Based Recommendations" in prompt or "weather" in prompt.lower()
        assert "Must-Visit Places" in prompt or "places" in prompt.lower()
        assert "Activities" in prompt or "activities" in prompt.lower()
    
    @pytest.mark.asyncio
    async def test_itinerary_prompt_different_days(self):
        """Test prompt adapts to different day counts."""
        prompt_1 = await get_itinerary_prompt(1, "2025-01-15")
        prompt_7 = await get_itinerary_prompt(7, "2025-01-15")
        
        assert "1-day" in prompt_1.lower() or "1 day" in prompt_1.lower()
        assert "7-day" in prompt_7.lower() or "7 day" in prompt_7.lower()


@pytest.mark.unit
class TestGetWeatherBasedActivitiesPrompt:
    """Test weather-based activities prompt generation."""
    
    @pytest.mark.asyncio
    async def test_weather_prompt_structure(self, sample_weather_data):
        """Test that weather prompt has correct structure."""
        prompt = await get_weather_based_activities_prompt(sample_weather_data)
        
        assert isinstance(prompt, str)
        assert "weather forecast" in prompt.lower() or "weather" in prompt.lower()
        assert "Cox's Bazar" in prompt or sample_weather_data["location"] in prompt
    
    @pytest.mark.asyncio
    async def test_weather_prompt_includes_forecast_data(self, sample_weather_data):
        """Test that prompt includes essential weather information."""
        prompt = await get_weather_based_activities_prompt(sample_weather_data)
        
        # Check for key weather fields
        assert "Temperature" in prompt or "temperature" in prompt.lower()
        assert "Precipitation" in prompt or "precipitation" in prompt.lower()
        assert "Wind Speed" in prompt or "wind" in prompt.lower()
    
    @pytest.mark.asyncio
    async def test_weather_prompt_includes_daily_summary(self, sample_weather_data):
        """Test that prompt includes day-by-day breakdown."""
        prompt = await get_weather_based_activities_prompt(sample_weather_data)
        
        # Should include day numbers
        assert "Day 1" in prompt or "day 1" in prompt.lower()
        assert "Day 2" in prompt or "day 2" in prompt.lower()
    
    @pytest.mark.asyncio
    async def test_weather_prompt_empty_forecast(self):
        """Test graceful handling of empty forecast data."""
        empty_data = {
            "location": "Cox's Bazar",
            "days": 0,
            "start_date": "2025-01-15",
            "forecast": []
        }
        
        prompt = await get_weather_based_activities_prompt(empty_data)
        
        assert isinstance(prompt, str)
        assert "Cox's Bazar" in prompt
    
    @pytest.mark.asyncio
    async def test_weather_prompt_missing_fields(self):
        """Test prompt generation with minimal required fields."""
        minimal_data = {
            "forecast": [
                {
                    "day": 1,
                    "date": "2025-01-15",
                    "weather": "Clear sky",
                    "temp_min": 25.0,
                    "temp_max": 30.0,
                    "temp_avg": 27.5,
                    "precipitation": 0.0,
                    "windspeed": 15.0,
                    "sunrise": "06:00",
                    "sunset": "18:00",
                }
            ]
        }
        
        prompt = await get_weather_based_activities_prompt(minimal_data)
        
        assert isinstance(prompt, str)
        # Should handle missing fields gracefully
        assert "Day 1" in prompt or "day 1" in prompt.lower()

