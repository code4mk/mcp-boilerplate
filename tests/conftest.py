"""Pytest configuration and shared fixtures.

This file imports all fixtures from the fixtures/ directory to make them
available to all tests. Additional pytest configuration and hooks can be
added here as needed.
"""
# Import all fixtures to make them available to tests
from tests.fixtures import (
    mock_context,
    sample_weather_data,
    mock_open_meteo_response,
)

__all__ = [
    "mock_context",
    "sample_weather_data",
    "mock_open_meteo_response",
]
