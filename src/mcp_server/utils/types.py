"""Type definitions for MCP server configuration."""

from typing import TypedDict, Literal, Collection, Any
from mcp.types import Icon


class FastMCPConfigDict(TypedDict, total=False):
    """Configuration dictionary for FastMCP server initialization.
    
    This TypedDict provides type hints for FastMCP configuration options.
    All fields are optional (total=False) to allow partial configuration.
    """
    
    # Basic server information
    name: str
    instructions: str
    website_url: str
    icons: list[Icon]
    
    # Server settings
    debug: bool
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    host: str
    port: int
    
    # Path configurations
    mount_path: str
    sse_path: str
    message_path: str
    streamable_http_path: str
    
    # Behavior flags
    json_response: bool
    stateless_http: bool
    warn_on_duplicate_resources: bool
    warn_on_duplicate_tools: bool
    warn_on_duplicate_prompts: bool
    
    # Dependencies
    dependencies: Collection[str]

