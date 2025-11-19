"""Unit tests for Pydantic models."""
import pytest
from pydantic import ValidationError
from mcp_server.models.itinerary_models import ItineraryPreferences


@pytest.mark.unit
class TestItineraryPreferences:
    """Test ItineraryPreferences model validation and behavior."""
    
    def test_valid_preferences(self):
        """Test creating valid preferences with all fields."""
        prefs = ItineraryPreferences(extendTrip=True, newDays=3)
        
        assert prefs.extendTrip is True
        assert prefs.newDays == 3
    
    def test_default_values(self):
        """Test that default values are applied correctly."""
        prefs = ItineraryPreferences(extendTrip=False)
        
        assert prefs.extendTrip is False
        assert prefs.newDays == 2  # Default value
    
    def test_custom_days(self):
        """Test setting custom number of days."""
        prefs = ItineraryPreferences(extendTrip=True, newDays=5)
        
        assert prefs.newDays == 5
    
    def test_minimum_days(self):
        """Test that various day values are accepted."""
        # Pydantic doesn't enforce minimum by default in this model
        # But we can test that it accepts various values
        prefs = ItineraryPreferences(extendTrip=True, newDays=1)
        assert prefs.newDays == 1
        
        prefs = ItineraryPreferences(extendTrip=True, newDays=10)
        assert prefs.newDays == 10
    
    def test_from_dict(self):
        """Test creating model instance from dictionary."""
        data = {"extendTrip": True, "newDays": 4}
        prefs = ItineraryPreferences(**data)
        
        assert prefs.extendTrip is True
        assert prefs.newDays == 4
    
    def test_to_dict(self):
        """Test serializing model to dictionary."""
        prefs = ItineraryPreferences(extendTrip=True, newDays=3)
        prefs_dict = prefs.model_dump()
        
        assert prefs_dict["extendTrip"] is True
        assert prefs_dict["newDays"] == 3

