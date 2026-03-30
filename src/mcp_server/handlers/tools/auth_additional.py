from mcp_server.mcp_instance import mcp
from mcp_server.utils.helpers import (
    require_premium_user, require_permissions, get_client_ip,
    get_user_agent, get_mcp_session_id, get_auth0_user_info
)
from fastmcp import Context
from fastmcp.server.dependencies import get_access_token
from dotenv import load_dotenv
import os

load_dotenv()

@mcp.tool(
    name="get_user_info",
    description="Return auth user info",
    auth=require_permissions("tool:get_user_info")
)
async def get_user_info() -> dict:
    """Returns information about the authenticated GitHub user."""
    
    token = get_access_token()
    output = {}
    auth_provider = os.environ.get("AUTH_PROVIDER", "github")
    
    if auth_provider == "auth0":
        output = {
            "issuer": token.claims.get("iss"),
            "audience": token.claims.get("aud"),
            "scope": token.claims.get("scope"),
            "permissions": token.claims.get("permissions"),
            "user_info": get_auth0_user_info(token.token)
        }
    elif auth_provider == "github":
        output = {
            "github_user": token.claims.get("login"),
            "name": token.claims.get("name"),
            "email": token.claims.get("email")
        }
    return output

@mcp.tool(
    name="custom_auth_tool",
    description="Custom auth tool",
    auth=require_premium_user
)
async def custom_auth_tool() -> dict:
    """Custom auth tool"""
    token = get_access_token()
    print(token)
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