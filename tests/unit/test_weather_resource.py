"""Unit tests for weather resource endpoint."""
import pytest
import sys
from unittest.mock import patch


@pytest.fixture
def resource_weather_forecast_func():
    """Fixture to get the undecorated weather resource function.
    
    This fixture patches the decorator to get direct access to the
    underlying function for unit testing.
    
    Yields:
        tuple: (function, module) pair for testing
    """
    # Patch the decorator to return the function as-is (no-op decorator)
    decorator_patcher = patch(
        'mcp_server.mcp_instance.mcp.resource',
        lambda *args, **kwargs: lambda f: f
    )
    decorator_patcher.start()
    
    try:
        # Clear module cache and re-import to get undecorated function
        if 'mcp_server.components.resources.weather' in sys.modules:
            del sys.modules['mcp_server.components.resources.weather']
        from mcp_server.components.resources import weather
        yield weather.resource_weather_forecast, weather
    finally:
        decorator_patcher.stop()
        # Clean up module cache
        if 'mcp_server.components.resources.weather' in sys.modules:
            del sys.modules['mcp_server.components.resources.weather']


@pytest.mark.unit
class TestWeatherResource:
    """Test weather resource endpoint behavior."""
    
    @pytest.mark.asyncio
    async def test_weather_resource_success(self, resource_weather_forecast_func):
        """Test successful weather resource data retrieval."""
        func, weather_module = resource_weather_forecast_func
        
        # Patch the function in the module where it's used
        with patch.object(weather_module, 'get_weather_forecast') as mock_forecast:
            mock_data = {
                "location": "Cox's Bazar, Bangladesh",
                "start_date": "2025-01-15",
                "days": 3,
                "forecast": []
            }
            mock_forecast.return_value = mock_data
            
            result = await func("2025-01-15", 3)
            
            assert result == mock_data
            mock_forecast.assert_called_once_with("2025-01-15", 3)
    
    @pytest.mark.asyncio
    async def test_weather_resource_today(self, resource_weather_forecast_func):
        """Test weather resource with 'today' as date parameter."""
        func, weather_module = resource_weather_forecast_func
        
        # Patch the function in the module where it's used
        with patch.object(weather_module, 'get_weather_forecast') as mock_forecast:
            mock_data = {
                "location": "Cox's Bazar, Bangladesh",
                "start_date": "2025-01-15",
                "days": 1,
                "forecast": []
            }
            mock_forecast.return_value = mock_data
            
            result = await func("today", 1)
            
            assert result == mock_data
            mock_forecast.assert_called_once_with("today", 1)
    
    @pytest.mark.asyncio
    async def test_weather_resource_different_days(self, resource_weather_forecast_func):
        """Test weather resource with various day counts."""
        func, weather_module = resource_weather_forecast_func
        
        # Patch the function in the module where it's used
        with patch.object(weather_module, 'get_weather_forecast') as mock_forecast:
            mock_data = {
                "location": "Cox's Bazar, Bangladesh",
                "start_date": "2025-01-15",
                "days": 7,
                "forecast": []
            }
            mock_forecast.return_value = mock_data
            
            result = await func("2025-01-15", 7)
            
            assert result["days"] == 7
            mock_forecast.assert_called_once_with("2025-01-15", 7)

