"""
MCP Handlers package.

This package contains all MCP handler registrations organized into:
- resources: Data fetching and resource functions
- prompts: AI prompt generation functions  
- tools: Tools that combine resources and prompts

All functions are designed to be importable and reusable.
"""

from mcp_server.handlers import resources, prompts, tools

__all__ = ["resources", "prompts", "tools"]

