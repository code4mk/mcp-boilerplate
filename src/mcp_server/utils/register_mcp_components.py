"""
Dynamic MCP Component Registration Utility.

Automatically discovers and imports all tools, prompts, and resources
from their respective component directories.
"""
import importlib
from pathlib import Path


def register_mcp_components(base_dir: Path, transport: str = "stdio") -> None:
    """
    Dynamically import all MCP components (tools, prompts, resources).
    
    This function scans the components directory and automatically imports
    all Python modules, which triggers their @mcp.tool(), @mcp.prompt(),
    and @mcp.resource() decorators.
    
    Args:
        mcp: The FastMCP instance to register components with
        base_dir: Base directory of the MCP server (usually Path(__file__).parent from server.py)
        transport: Transport type (default: "stdio"). If not "stdio", custom routes will be registered.
    """
    components_dir = base_dir / "components"
    component_types = ["tools", "prompts", "resources"]
    
    registered_count = {
        "tools": 0,
        "prompts": 0,
        "resources": 0
    }
    
    for component_type in component_types:
        component_path = components_dir / component_type
        
        if not component_path.exists():
            print(f"⚠️  Warning: {component_type} directory not found at {component_path}")
            continue
        
        # Find all Python files in the component directory
        python_files = [
            f for f in component_path.glob("*.py")
            if f.name != "__init__.py" and not f.name.startswith("_")
        ]
        
        for py_file in python_files:
            module_name = f"mcp_server.components.{component_type}.{py_file.stem}"
            
            try:
                # Import the module (this triggers the decorators)
                importlib.import_module(module_name)
                registered_count[component_type] += 1
                print(f"✅ Registered {component_type[:-1]}: {py_file.stem}")
            except Exception as e:
                print(f"❌ Error importing {module_name}: {e}")
                # Continue with other modules even if one fails
                continue
    
    # Register custom routes if transport is not stdio
    if transport.lower() != "stdio":
        try:
            config_path = base_dir / "config"
            custom_routes_file = config_path / "custom_routes.py"
            
            if custom_routes_file.exists():
                importlib.import_module("mcp_server.config.custom_routes")
                print(f"✅ Registered custom routes (transport: {transport})")
            else:
                print(f"⚠️  Warning: Custom routes file not found at {custom_routes_file}")
        except Exception as e:
            print(f"❌ Error importing custom routes: {e}")
    
    # Print summary
    print("\n📦 Registration Summary:")
    print(f"   🔧 Tools: {registered_count['tools']}")
    print(f"   💬 Prompts: {registered_count['prompts']}")
    print(f"   📚 Resources: {registered_count['resources']}")
    if transport.lower() != "stdio":
        print("   🛣️  Custom Routes: Enabled")
    print(f"   📊 Total: {sum(registered_count.values())} components registered\n")

