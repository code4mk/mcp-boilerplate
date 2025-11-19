"""MCP Context fixtures for testing."""
import pytest
from unittest.mock import Mock, AsyncMock
from fastmcp import Context


@pytest.fixture
def mock_context():
    """Create a mock MCP Context for testing.
    
    Returns:
        Mock: A mocked Context with async methods for testing MCP tools and resources.
        
    Example:
        >>> def test_my_tool(mock_context):
        ...     mock_context.info.assert_called_once()
    """
    ctx = Mock(spec=Context)
    ctx.read_resource = AsyncMock()
    ctx.info = AsyncMock()
    ctx.error = AsyncMock()
    ctx.elicit = AsyncMock()
    return ctx

