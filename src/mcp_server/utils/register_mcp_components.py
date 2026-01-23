"""
Dynamic MCP Component Registration Utility.

Automatically discovers and imports all tools, prompts, and resources
from their respective component directories.
"""
import importlib
import re
from pathlib import Path


def count_decorators_in_file(file_path: Path, component_type: str) -> int:
    """
    Count the number of MCP decorators in a Python file.
    
    Args:
        file_path: Path to the Python file
        component_type: Type of component ("tools", "prompts", or "resources")
    
    Returns:
        Number of decorators found
    """
    try:
        content = file_path.read_text()
        
        # Map component type to decorator pattern
        decorator_patterns = {
            "tools": r"@mcp\.tool\(",
            "prompts": r"@mcp\.prompt\(",
            "resources": r"@mcp\.resource\("
        }
        
        pattern = decorator_patterns.get(component_type)
        if not pattern:
            return 0
        
        # Filter out commented lines and count matches only in active code
        count = 0
        for line in content.split('\n'):
            stripped = line.strip()
            # Skip lines that are comments (start with #)
            if not stripped.startswith('#'):
                if re.search(pattern, line):
                    count += 1
        
        return count
    except Exception as e:
        print(f"Error counting decorators in {file_path}: {e}")
        return 0


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
            print(f"Warning: {component_type} directory not found at {component_path}")
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
                
                # Count decorators by reading the source file
                decorator_count = count_decorators_in_file(py_file, component_type)
                registered_count[component_type] += decorator_count
                
                print(f"Registered {component_type[:-1]} file: {py_file.stem} ({decorator_count} {component_type[:-1]}{'s' if decorator_count != 1 else ''})")
            except Exception as e:
                print(f"Error importing {module_name}: {e}")
                # Continue with other modules even if one fails
                continue
    
    # Register custom routes if transport is not stdio
    if transport.lower() != "stdio":
        try:
            config_path = base_dir / "config"
            custom_routes_file = config_path / "custom_routes.py"
            
            if custom_routes_file.exists():
                importlib.import_module("mcp_server.config.custom_routes")
                print(f"Registered custom routes (transport: {transport})")
            else:
                print(f"Warning: Custom routes file not found at {custom_routes_file}")
        except Exception as e:
            print(f"Error importing custom routes: {e}")
    
    # Print summary
    print("\n" + "="*50)
    print("Registration Summary:")
    print("="*50)
    print(f"Tools: {registered_count['tools']}")
    print(f"Prompts: {registered_count['prompts']}")
    print(f"Resources: {registered_count['resources']}")
    if transport.lower() != "stdio":
        print("Custom Routes: Enabled")
    print(f"\nTotal: {sum(registered_count.values())} components registered")
    print("="*50 + "\n")
