"""Main FastMCP server for Cox's Bazar AI Itinerary."""
import sys
import os
from pathlib import Path
# Add src directory to path if running directly
if __name__ == "__main__" or "mcp_server" not in sys.modules:
    src_path = Path(__file__).parent.parent  # This points to src/
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

from dotenv import load_dotenv
from mcp_server.utils.register_mcp_components import register_mcp_components
from mcp_server.mcp_instance import mcp


load_dotenv()



def main():
    """Run the MCP server."""
    transport_name = os.environ.get("TRANSPORT_NAME") or "stdio"
    server_port = int(os.environ.get("SERVER_PORT") or 8000)
    server_host = os.environ.get("SERVER_HOST") or "0.0.0.0"

    #Auto-register all MCP components (tools, prompts, resources)
    base_dir = Path(__file__).parent
    register_mcp_components(base_dir, transport=transport_name)
    
    if transport_name == "http" or transport_name == "streamable-http" or transport_name == "sse":
        mcp.run(transport=transport_name, port=server_port, host=server_host)
    else:
        mcp.run(transport=transport_name)
    
if __name__ == "__main__":
    main()