"""Pydantic models for itinerary tools."""
from pydantic import BaseModel, Field
from datetime import datetime

class ItineraryPreferences(BaseModel):
    """Schema for collecting user itinerary preferences."""
    extendTrip: bool = Field(
        description="Would you like to extend your trip to the recommended minimum of 2 days?"
    )
    newDays: int = Field(
        default=2,
        description="Number of days for the extended trip (minimum 2)",
    )

class GenerateItinerarySchema(BaseModel):
    """Schema for generating an itinerary."""
    start_date: str = Field(
        description="Start date of the trip",
        default="2026-01-24"
    )
    days: int = Field(
        description="Number of days for the trip",
        default=2
    )

class GetActivitySuggestionsSchema(BaseModel):
    """Schema for getting activity suggestions."""
    temperature: float = Field(
        description="Temperature in Celsius",
        default=28
    )
    time_of_day: str = Field(
        default="afternoon",
        description="Time of day (morning, afternoon, evening)"
    )