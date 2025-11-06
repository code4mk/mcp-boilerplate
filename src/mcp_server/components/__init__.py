"""
MCP Components package.

This package contains all MCP components organized into:
- resources: Data fetching and resource functions
- prompts: AI prompt generation functions  
- tools: Tools that combine resources and prompts

All functions are designed to be importable and reusable.
"""

from mcp_server.components import resources, prompts, tools

__all__ = ["resources", "prompts", "tools"]

