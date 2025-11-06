"""
Shared MCP instance for all modules.
"""
import os
from typing import Any
from mcp.server.fastmcp import FastMCP
from mcp_server.utils.types import FastMCPConfigDict
from dotenv import load_dotenv

load_dotenv()

# Get transport name and port from environment variables
transport_name = os.environ.get("TRANSPORT_NAME") or "stdio"
port = os.environ.get("PORT") or 8000

fast_mcp_config: FastMCPConfigDict = {
    "name": "Cox's Bazar AI Itinerary MCP"
}

if transport_name == "sse" or transport_name == "streamable-http":
    fast_mcp_config["host"] = "0.0.0.0"
    fast_mcp_config["port"] = int(port)

mcp = FastMCP[Any](**fast_mcp_config)
