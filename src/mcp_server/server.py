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

base_dir = Path(__file__).parent
transport_name = os.environ.get("TRANSPORT_NAME") or "stdio"
server_port = int(os.environ.get("SERVER_PORT") or 8000)

# Auto-register all MCP components (tools, prompts, resources)
register_mcp_components(base_dir, transport=transport_name)


def main():
    """Run the MCP server."""
    print("🌴 Starting Cox's Bazar AI Itinerary MCP server...")
    print("📍 Location: Cox's Bazar, Bangladesh")
    print("🚀 Server ready!")
    if not transport_name.lower() == "stdio":
        mcp.run(transport=transport_name, port=server_port, host="127.0.0.1")
    else:
        mcp.run(transport=transport_name)
    
    
if __name__ == "__main__":
    main()