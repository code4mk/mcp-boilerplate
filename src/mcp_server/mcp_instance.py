import os
from fastmcp import FastMCP
from mcp_server.config.auth_provider import get_auth_provider
from dotenv import load_dotenv


load_dotenv()

is_auth_enabled = os.environ.get("AUTH_ENABLED", "").lower() in ("true", "1")

# Configuration for MCP initialization
mcp_config_context = {
    "name": "Cox's Bazar AI Itinerary MCP",
}

# Add auth if auth is enabled
if is_auth_enabled:
    auth_provider = os.environ.get("AUTH_PROVIDER", "github")
    mcp_config_context["auth"] = get_auth_provider(auth_provider)


# Initialize FastMCP with valid parameters only
mcp = FastMCP(**mcp_config_context, strict_input_validation=True)

