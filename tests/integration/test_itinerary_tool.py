"""Integration tests for itinerary tool.

These tests verify the complete flow of itinerary generation including
elicitation, weather data retrieval, and prompt generation.
"""
import pytest
import json
import sys
from unittest.mock import AsyncMock, Mock, patch


@pytest.fixture
def cox_ai_itinerary_func():
    """Fixture to get the underlying cox_ai_itinerary function.
    
    This fixture bypasses the decorator to enable direct testing
    of the itinerary generation logic.
    
    Yields:
        function: The undecorated cox_ai_itinerary function
    """
    # Patch the decorator to return the function as-is (no-op decorator)
    decorator_patcher = patch(
        'mcp_server.mcp_instance.mcp.tool',
        lambda **kwargs: lambda f: f
    )
    decorator_patcher.start()
    
    try:
        # Clear module cache and re-import to get undecorated function
        if 'mcp_server.components.tools.itinerary' in sys.modules:
            del sys.modules['mcp_server.components.tools.itinerary']
        from mcp_server.components.tools import itinerary
        yield itinerary.cox_ai_itinerary
    finally:
        decorator_patcher.stop()
        # Clean up module cache
        if 'mcp_server.components.tools.itinerary' in sys.modules:
            del sys.modules['mcp_server.components.tools.itinerary']


@pytest.mark.integration
class TestCoxAiItinerary:
    """Test complete itinerary generation workflow."""
    
    @pytest.mark.asyncio
    async def test_itinerary_generation_success(
        self, mock_context, sample_weather_data, cox_ai_itinerary_func
    ):
        """Test successful end-to-end itinerary generation."""
        # Mock elicitation (trip meets minimum days)
        mock_context.elicit = AsyncMock(side_effect=NotImplementedError())
        
        # Mock resource reading
        weather_json = json.dumps(sample_weather_data)
        mock_context.read_resource.return_value = [
            Mock(content=weather_json)
        ]
        
        # Mock prompt generation
        with patch("mcp_server.components.tools.itinerary.get_itinerary_prompt") as mock_prompt, \
             patch("mcp_server.components.tools.itinerary.get_weather_based_activities_prompt") as mock_weather_prompt:
            
            mock_prompt.return_value = "Base itinerary prompt"
            mock_weather_prompt.return_value = "Weather-based prompt"
            
            result = await cox_ai_itinerary_func(mock_context, "2025-01-15", 3)
            
            assert isinstance(result, str)
            assert "Cox's Bazar Itinerary Planning" in result
            assert "Trip Details" in result
            assert "Weather Forecast" in result
            assert "3 day(s)" in result
            mock_context.read_resource.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_itinerary_with_elicitation(
        self, mock_context, sample_weather_data, cox_ai_itinerary_func
    ):
        """Test itinerary generation with trip extension via elicitation."""
        # Mock successful elicitation
        mock_result = Mock()
        mock_result.action = "accept"
        mock_result.data = Mock()
        mock_result.data.extendTrip = True
        mock_result.data.newDays = 3
        
        mock_context.elicit.return_value = mock_result
        mock_context.read_resource.return_value = [
            Mock(content=json.dumps(sample_weather_data))
        ]
        
        with patch("mcp_server.components.tools.itinerary.get_itinerary_prompt") as mock_prompt, \
             patch("mcp_server.components.tools.itinerary.get_weather_based_activities_prompt") as mock_weather_prompt:
            
            mock_prompt.return_value = "Base prompt"
            mock_weather_prompt.return_value = "Weather prompt"
            
            result = await cox_ai_itinerary_func(mock_context, "2025-01-15", 1)
            
            assert "3 day(s)" in result
            mock_context.elicit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_itinerary_elicitation_cancelled(
        self, mock_context, cox_ai_itinerary_func
    ):
        """Test itinerary generation when user cancels elicitation."""
        mock_result = Mock()
        mock_result.action = "accept"
        mock_result.data = Mock()
        mock_result.data.extendTrip = False
        
        mock_context.elicit.return_value = mock_result
        
        result = await cox_ai_itinerary_func(mock_context, "2025-01-15", 1)
        
        assert "CANCELLED" in result or "Error" in result
        mock_context.error.assert_called()
    
    @pytest.mark.asyncio
    async def test_itinerary_invalid_date(
        self, mock_context, sample_weather_data, cox_ai_itinerary_func
    ):
        """Test itinerary generation with invalid date input."""
        mock_context.elicit = AsyncMock(side_effect=NotImplementedError())
        mock_context.read_resource.return_value = [
            Mock(content=json.dumps(sample_weather_data))
        ]
        
        with patch("mcp_server.components.tools.itinerary.get_itinerary_prompt") as mock_prompt, \
             patch("mcp_server.components.tools.itinerary.get_weather_based_activities_prompt") as mock_weather_prompt:
            
            mock_prompt.return_value = "Base prompt"
            mock_weather_prompt.return_value = "Weather prompt"
            
            # Invalid date should default to today
            result = await cox_ai_itinerary_func(mock_context, "invalid-date", 3)
            
            assert isinstance(result, str)
            assert "Cox's Bazar Itinerary Planning" in result
    
    @pytest.mark.asyncio
    async def test_itinerary_weather_forecast_format(
        self, mock_context, sample_weather_data, cox_ai_itinerary_func
    ):
        """Test that itinerary includes properly formatted weather data."""
        mock_context.elicit = AsyncMock(side_effect=NotImplementedError())
        mock_context.read_resource.return_value = [
            Mock(content=json.dumps(sample_weather_data))
        ]
        
        with patch("mcp_server.components.tools.itinerary.get_itinerary_prompt") as mock_prompt, \
             patch("mcp_server.components.tools.itinerary.get_weather_based_activities_prompt") as mock_weather_prompt:
            
            mock_prompt.return_value = "Base prompt"
            mock_weather_prompt.return_value = "Weather prompt"
            
            result = await cox_ai_itinerary_func(mock_context, "2025-01-15", 3)
            
            # Check that weather data is included
            assert "Temperature" in result
            assert "Weather:" in result
            assert "Precipitation:" in result
            assert "Wind Speed:" in result
            assert "Sunrise:" in result
            assert "Sunset:" in result
            assert "Activity Suggestions:" in result
    
    @pytest.mark.asyncio
    async def test_itinerary_activity_suggestions_included(
        self, mock_context, sample_weather_data, cox_ai_itinerary_func
    ):
        """Test that activity suggestions are properly integrated."""
        mock_context.elicit = AsyncMock(side_effect=NotImplementedError())
        mock_context.read_resource.return_value = [
            Mock(content=json.dumps(sample_weather_data))
        ]
        
        with patch("mcp_server.components.tools.itinerary.get_itinerary_prompt") as mock_prompt, \
             patch("mcp_server.components.tools.itinerary.get_weather_based_activities_prompt") as mock_weather_prompt:
            
            mock_prompt.return_value = "Base prompt"
            mock_weather_prompt.return_value = "Weather prompt"
            
            result = await cox_ai_itinerary_func(mock_context, "2025-01-15", 3)
            
            # Check for activity suggestions by time of day
            assert "Morning:" in result
            assert "Afternoon:" in result
            assert "Evening:" in result


@pytest.mark.integration
class TestGetActivitySuggestions:
    """Test activity suggestions utility function."""
    
    def test_get_activity_suggestions_morning(self):
        """Test morning activity suggestions."""
        from mcp_server.utils.get_weather_forecast import (
            get_activity_suggestions as get_suggestions_impl
        )
        
        result = get_suggestions_impl(25.0, "morning")
        
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(activity, str) for activity in result)
    
    def test_get_activity_suggestions_afternoon(self):
        """Test afternoon activity suggestions."""
        from mcp_server.utils.get_weather_forecast import (
            get_activity_suggestions as get_suggestions_impl
        )
        
        result = get_suggestions_impl(28.0, "afternoon")
        
        assert isinstance(result, list)
        assert len(result) > 0
    
    def test_get_activity_suggestions_evening(self):
        """Test evening activity suggestions."""
        from mcp_server.utils.get_weather_forecast import (
            get_activity_suggestions as get_suggestions_impl
        )
        
        result = get_suggestions_impl(27.0, "evening")
        
        assert isinstance(result, list)
        assert len(result) > 0

