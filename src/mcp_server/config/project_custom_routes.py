from mcp_server.mcp_instance import mcp
from starlette.responses import JSONResponse, PlainTextResponse

@mcp.custom_route("/", methods=["GET"])
async def root(request):
    """Root endpoint for health check."""
    return JSONResponse({
        "message": "Hello, World!",
        "service": "Cox's Bazar AI Itinerary MCP Server",
        "status": "running"
    })

@mcp.custom_route("/health", methods=["GET"])
async def health(request):
    """Health check endpoint."""
    return PlainTextResponse("OK")