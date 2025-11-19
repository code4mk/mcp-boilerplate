"""Integration tests for weather API interactions."""
import pytest
from unittest.mock import Mock, patch
from mcp_server.utils.get_weather_forecast import get_weather_forecast


@pytest.mark.integration
class TestWeatherForecastAPI:
    """Test weather forecast API integration and error handling."""
    
    @patch("mcp_server.utils.get_weather_forecast.requests.get")
    def test_successful_forecast(self, mock_get, mock_open_meteo_response):
        """Test successful weather forecast retrieval from API."""
        mock_response = Mock()
        mock_response.json.return_value = mock_open_meteo_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = get_weather_forecast("2025-01-15", 3)
        
        assert result["location"] == "Cox's Bazar, Bangladesh"
        assert result["days"] == 3
        assert len(result["forecast"]) == 3
        assert result["forecast"][0]["day"] == 1
        assert "temp_max" in result["forecast"][0]
        assert "temp_min" in result["forecast"][0]
        assert "temp_avg" in result["forecast"][0]
    
    @patch("mcp_server.utils.get_weather_forecast.requests.get")
    def test_api_error_response(self, mock_get):
        """Test handling of API error responses."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "error": True,
            "reason": "Invalid date range"
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = get_weather_forecast("2025-01-15", 3)
        
        # Should fallback to mock data
        assert "note" in result or result["days"] == 3
    
    @patch("mcp_server.utils.get_weather_forecast.requests.get")
    def test_api_request_failure(self, mock_get):
        """Test handling of network failures."""
        mock_get.side_effect = Exception("Network error")
        
        result = get_weather_forecast("2025-01-15", 3)
        
        # Should fallback to mock data
        assert result["days"] == 3
        assert len(result["forecast"]) == 3
    
    def test_today_date_parsing(self):
        """Test parsing 'today' as start date parameter."""
        with patch("mcp_server.utils.get_weather_forecast.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "daily": {
                    "time": ["2025-01-15"],
                    "temperature_2m_max": [30.0],
                    "temperature_2m_min": [25.0],
                    "precipitation_sum": [0.0],
                    "weathercode": [0],
                    "windspeed_10m_max": [15.0],
                    "sunrise": ["2025-01-15T06:00"],
                    "sunset": ["2025-01-15T18:00"],
                }
            }
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            result = get_weather_forecast("today", 1)
            assert result["days"] == 1
    
    def test_invalid_date_parsing(self):
        """Test handling of invalid date formats."""
        with patch("mcp_server.utils.get_weather_forecast.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "daily": {
                    "time": ["2025-01-15"],
                    "temperature_2m_max": [30.0],
                    "temperature_2m_min": [25.0],
                    "precipitation_sum": [0.0],
                    "weathercode": [0],
                    "windspeed_10m_max": [15.0],
                    "sunrise": ["2025-01-15T06:00"],
                    "sunset": ["2025-01-15T18:00"],
                }
            }
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            # Invalid date should default to today
            result = get_weather_forecast("invalid-date", 1)
            assert result["days"] == 1
    
    @patch("mcp_server.utils.get_weather_forecast.requests.get")
    def test_forecast_date_range(self, mock_get, mock_open_meteo_response):
        """Test forecast retrieval with different date ranges."""
        mock_response = Mock()
        mock_response.json.return_value = mock_open_meteo_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Test 1 day
        result = get_weather_forecast("2025-01-15", 1)
        assert result["days"] == 1
        
        # Test 7 days
        mock_open_meteo_response["daily"]["time"] = [
            f"2025-01-{15+i}" for i in range(7)
        ]
        mock_open_meteo_response["daily"]["temperature_2m_max"] = [30.0] * 7
        mock_open_meteo_response["daily"]["temperature_2m_min"] = [25.0] * 7
        mock_open_meteo_response["daily"]["precipitation_sum"] = [0.0] * 7
        mock_open_meteo_response["daily"]["weathercode"] = [0] * 7
        mock_open_meteo_response["daily"]["windspeed_10m_max"] = [15.0] * 7
        mock_open_meteo_response["daily"]["sunrise"] = [
            f"2025-01-{15+i}T06:00" for i in range(7)
        ]
        mock_open_meteo_response["daily"]["sunset"] = [
            f"2025-01-{15+i}T18:00" for i in range(7)
        ]
        
        result = get_weather_forecast("2025-01-15", 7)
        assert result["days"] == 7
        assert len(result["forecast"]) == 7

