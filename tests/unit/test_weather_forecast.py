"""Unit tests for weather forecast utility functions."""
import pytest
from mcp_server.utils.get_weather_forecast import (
    get_weather_description,
    get_fallback_forecast,
    get_activity_suggestions,
)


@pytest.mark.unit
class TestWeatherDescription:
    """Test weather code to human-readable description conversion."""
    
    def test_clear_sky(self):
        """Test clear sky weather code mapping."""
        assert get_weather_description(0) == "Clear sky"
    
    def test_rainy_weather(self):
        """Test various rain intensity codes."""
        assert get_weather_description(61) == "Slight rain"
        assert get_weather_description(63) == "Moderate rain"
        assert get_weather_description(65) == "Heavy rain"
    
    def test_thunderstorm(self):
        """Test thunderstorm weather code."""
        assert get_weather_description(95) == "Thunderstorm"
    
    def test_unknown_code(self):
        """Test handling of unrecognized weather codes."""
        assert get_weather_description(999) == "Unknown"


@pytest.mark.unit
class TestActivitySuggestions:
    """Test activity suggestions based on temperature and time of day."""
    
    def test_morning_cool_weather(self):
        """Test morning activities for comfortable temperatures (<28°C)."""
        suggestions = get_activity_suggestions(25.0, "morning")
        assert len(suggestions) > 0
        assert "Beach walk" in suggestions[0] or "Himchari" in suggestions[0]
    
    def test_morning_warm_weather(self):
        """Test morning activities for warm weather (>=28°C)."""
        suggestions = get_activity_suggestions(30.0, "morning")
        assert len(suggestions) > 0
        assert any("swim" in s.lower() or "beach" in s.lower() for s in suggestions)
    
    def test_afternoon_cool_weather(self):
        """Test afternoon activities for moderate temperatures (<30°C)."""
        suggestions = get_activity_suggestions(28.0, "afternoon")
        assert len(suggestions) > 0
        assert any("monastery" in s.lower() or "village" in s.lower() for s in suggestions)
    
    def test_afternoon_hot_weather(self):
        """Test afternoon activities for hot weather (>=30°C)."""
        suggestions = get_activity_suggestions(32.0, "afternoon")
        assert len(suggestions) > 0
        assert any("indoor" in s.lower() or "shopping" in s.lower() for s in suggestions)
    
    def test_evening_activities(self):
        """Test evening activities (temperature independent)."""
        suggestions = get_activity_suggestions(27.0, "evening")
        assert len(suggestions) > 0
        assert any("sunset" in s.lower() or "dinner" in s.lower() for s in suggestions)
    
    def test_default_time_of_day(self):
        """Test default time of day fallback (afternoon)."""
        suggestions = get_activity_suggestions(28.0)
        assert len(suggestions) > 0


@pytest.mark.unit
class TestFallbackForecast:
    """Test fallback forecast generation for offline scenarios."""
    
    def test_fallback_forecast_structure(self):
        """Test that fallback forecast has all required fields."""
        start_date = "2025-01-15"
        end_date = "2025-01-17"
        days = 3
        
        forecast = get_fallback_forecast(start_date, end_date, days)
        
        assert forecast["location"] == "Cox's Bazar, Bangladesh"
        assert forecast["start_date"] == start_date
        assert forecast["end_date"] == end_date
        assert forecast["days"] == days
        assert forecast["timezone"] == "Asia/Dhaka"
        assert len(forecast["forecast"]) == days
        assert "note" in forecast
    
    def test_fallback_forecast_days(self):
        """Test fallback forecast generates correct number of day entries."""
        start_date = "2025-01-15"
        end_date = "2025-01-20"
        days = 6
        
        forecast = get_fallback_forecast(start_date, end_date, days)
        
        assert len(forecast["forecast"]) == days
        assert forecast["forecast"][0]["day"] == 1
        assert forecast["forecast"][-1]["day"] == days
    
    def test_fallback_forecast_data_types(self):
        """Test that fallback forecast uses correct data types."""
        forecast = get_fallback_forecast("2025-01-15", "2025-01-17", 3)
        
        day = forecast["forecast"][0]
        assert isinstance(day["day"], int)
        assert isinstance(day["temp_max"], (int, float))
        assert isinstance(day["temp_min"], (int, float))
        assert isinstance(day["temp_avg"], (int, float))
        assert isinstance(day["precipitation"], (int, float))
        assert isinstance(day["weather"], str)

