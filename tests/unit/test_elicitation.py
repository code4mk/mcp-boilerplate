"""Unit tests for elicitation utilities."""
import pytest
from unittest.mock import AsyncMock, Mock
from mcp_server.utils.elicitation import elicit_trip_extension
from mcp_server.models.itinerary_models import ItineraryPreferences


@pytest.mark.unit
class TestElicitTripExtension:
    """Test trip extension elicitation logic and edge cases."""
    
    @pytest.mark.asyncio
    async def test_no_elicitation_needed(self, mock_context):
        """Test when trip days already meet minimum requirement."""
        days, note = await elicit_trip_extension(
            mock_context, "2025-01-15", 3, min_days=2
        )
        
        assert days == 3
        assert note == ""
        mock_context.elicit.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_elicitation_accepted_with_extension(self, mock_context):
        """Test successful trip extension via elicitation."""
        # Mock elicitation response
        mock_result = Mock()
        mock_result.action = "accept"
        mock_result.data = Mock(spec=ItineraryPreferences)
        mock_result.data.extendTrip = True
        mock_result.data.newDays = 3
        
        mock_context.elicit.return_value = mock_result
        
        days, note = await elicit_trip_extension(
            mock_context, "2025-01-15", 1, min_days=2
        )
        
        assert days == 3
        assert note == ""
        mock_context.elicit.assert_called_once()
        mock_context.info.assert_called()
    
    @pytest.mark.asyncio
    async def test_elicitation_accepted_with_minimum_days(self, mock_context):
        """Test that minimum days constraint is enforced."""
        mock_result = Mock()
        mock_result.action = "accept"
        mock_result.data = Mock(spec=ItineraryPreferences)
        mock_result.data.extendTrip = True
        mock_result.data.newDays = 1  # Below minimum
        
        mock_context.elicit.return_value = mock_result
        
        days, note = await elicit_trip_extension(
            mock_context, "2025-01-15", 1, min_days=2
        )
        
        # Should enforce minimum days
        assert days == 2
        assert note == ""
    
    @pytest.mark.asyncio
    async def test_elicitation_rejected(self, mock_context):
        """Test when user rejects trip extension."""
        mock_result = Mock()
        mock_result.action = "accept"
        mock_result.data = Mock(spec=ItineraryPreferences)
        mock_result.data.extendTrip = False
        
        mock_context.elicit.return_value = mock_result
        
        with pytest.raises(ValueError, match="CANCELLED"):
            await elicit_trip_extension(mock_context, "2025-01-15", 1, min_days=2)
    
    @pytest.mark.asyncio
    async def test_elicitation_cancelled(self, mock_context):
        """Test when user cancels elicitation dialog."""
        mock_result = Mock()
        mock_result.action = "cancel"
        
        mock_context.elicit.return_value = mock_result
        
        with pytest.raises(ValueError, match="CANCELLED"):
            await elicit_trip_extension(mock_context, "2025-01-15", 1, min_days=2)
    
    @pytest.mark.asyncio
    async def test_elicitation_not_supported(self, mock_context):
        """Test graceful handling when client doesn't support elicitation."""
        mock_context.elicit.side_effect = NotImplementedError(
            "Elicitation not supported"
        )
        
        days, note = await elicit_trip_extension(
            mock_context, "2025-01-15", 1, min_days=2
        )
        
        assert days == 1
        assert "NOTE" in note
        assert "does not support interactive elicitation" in note
        mock_context.error.assert_called()
    
    @pytest.mark.asyncio
    async def test_elicitation_attribute_error(self, mock_context):
        """Test handling of AttributeError when elicit method is missing."""
        mock_context.elicit.side_effect = AttributeError("No elicit method")
        
        days, note = await elicit_trip_extension(
            mock_context, "2025-01-15", 1, min_days=2
        )
        
        assert days == 1
        assert "NOTE" in note
    
    @pytest.mark.asyncio
    async def test_elicitation_exception_handling(self, mock_context):
        """Test graceful handling of unexpected exceptions."""
        mock_context.elicit.side_effect = Exception("Unexpected error")
        
        days, note = await elicit_trip_extension(
            mock_context, "2025-01-15", 1, min_days=2
        )
        
        assert days == 1
        assert "NOTE" in note
    
    @pytest.mark.asyncio
    async def test_value_error_propagation(self, mock_context):
        """Test that ValueError (cancellation) is properly re-raised."""
        mock_context.elicit.side_effect = ValueError("User cancelled")
        
        with pytest.raises(ValueError):
            await elicit_trip_extension(mock_context, "2025-01-15", 1, min_days=2)

