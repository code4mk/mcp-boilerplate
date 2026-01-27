import os
from fastmcp import FastMCP
from mcp_server.config.auth_provider import get_auth_provider
from dotenv import load_dotenv


load_dotenv()

is_oauth_enabled = os.environ.get("IS_OAUTH_ENABLED") == "true"
# Configuration for MCP initialization
mcp_config_context = {
    "name": "Cox's Bazar AI Itinerary MCP",
}

# Add auth if OAuth is enabled
if is_oauth_enabled:
    mcp_config_context["auth"] = get_auth_provider("github")


# Initialize FastMCP with valid parameters only
mcp = FastMCP(**mcp_config_context, strict_input_validation=True)

