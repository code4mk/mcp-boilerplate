from mcp_server.mcp_instance import mcp
from fastmcp.server.auth import require_scopes
from mcp_server.utils.helpers import (
    require_premium_user, get_client_ip,
    get_user_agent, get_mcp_session_id
)
from fastmcp import Context
from fastmcp.server.dependencies import get_access_token

@mcp.tool(
    name="get_user_info",
    description="Return auth user info",
    auth=require_scopes("user")
)
async def get_user_info() -> dict:
    """Returns information about the authenticated GitHub user."""
    
    
    token = get_access_token()

    # The GitHubProvider stores user data in token claims
    return {
        "github_user": token.claims.get("login"),
        "name": token.claims.get("name"),
        "email": token.claims.get("email")
    }

@mcp.tool(
    name="custom_auth_tool",
    description="Custom auth tool",
    auth=require_premium_user
)
async def custom_auth_tool() -> dict:
    """Custom auth tool"""
    return {
        "message": "Custom auth tool"
    }

@mcp.tool
async def request_info(ctx: Context) -> dict:
    """Return information about the current request."""
    return {
        "request_id": ctx.request_id,
        "client_id": ctx.client_id or "Unknown client",
        "client_ip": get_client_ip(),
        "user_agent": get_user_agent(),
        "session_id": get_mcp_session_id()
    }