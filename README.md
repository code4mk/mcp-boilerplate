# Cox's Bazar AI Itinerary MCP Server

A Model Context Protocol (MCP) server that provides travel planning tools and weather information for Cox's Bazar, Bangladesh.

<a href="https://glama.ai/mcp/servers/@code4mk/coxs-bazar-itinerary-mcp-server">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@code4mk/coxs-bazar-itinerary-mcp-server/badge" alt="Cox's Bazar AI Itinerary Server MCP server" />
</a>

## Features

- **Weather Tools**: Get temperature forecasts and detailed weather information
- **Itinerary Tools**: Generate AI-powered travel itineraries
- **Travel Prompts**: Pre-configured prompts for travel planning

## Installation

```bash
uv sync
```

## Usage

### Run Inspector Tool

* Need node version > 20.x.x

```bash
./scripts/run-inspector.sh
```

### Run as installed command
```bash
uv run cox-mcp-server

# script 
./scripts/run-script.sh
```


## Requirements

- Python 3.13+
- mcp[cli] >= 1.20.0
- python-dateutil >= 2.9.0
- requests >= 2.32.5

## Project Structure

```
.
├── src/
│   └── mcp_server/
│       ├── __init__.py
│       ├── server.py           # Main server entry point
│       ├── mcp_instance.py     # MCP instance configuration
│       ├── models/             # Pydantic models and schemas
│       │   ├── __init__.py
│       │   └── itinerary_models.py  # Itinerary data models
│       ├── components/         # MCP components
│       │   ├── __init__.py
│       │   ├── tools/          # MCP tools
│       │   │   ├── __init__.py
│       │   │   ├── auth_user.py    # User authentication tool
│       │   │   └── itinerary.py    # Travel itinerary tools
│       │   ├── resources/      # MCP resources
│       │   │   ├── __init__.py
│       │   │   └── weather.py      # Weather data resources
│       │   └── prompts/        # MCP prompts
│       │       ├── __init__.py
│       │       └── travel_prompts.py  # Travel planning prompts
│       ├── config/             # Configuration modules
│       │   ├── auth_provider.py    # Authentication provider
│       │   └── custom_routes.py    # Custom routes configuration
│       ├── core/               # Core functionality
│       │   ├── __init__.py
│       │   └── prompts/
│       │       ├── __init__.py
│       │       └── get_travel_prompts.py  # Travel prompt handlers
│       └── utils/              # Utilities
│           ├── __init__.py
│           ├── elicitation.py  # Elicitation utilities
│           ├── get_weather_forecast.py  # Weather forecast utilities
│           ├── helpers.py      # Helper functions
│           ├── types.py        # Type definitions
│           └── register_mcp_components.py  # MCP component registration
├── scripts/                    # Shell scripts
│   ├── run-inspector.sh        # Run MCP inspector
│   └── run-script.sh           # Run server script
├── tests/                      # Test directory
├── _docs/                      # Documentation files
│   └── remote-mcp-connect.md   # Remote MCP connection guide
├── cox-mcp.jpeg                # Project image
├── Dockerfile                  # Docker configuration
├── glama.json                  # Glama configuration
├── README.md                   # Project documentation
├── license                     # MIT License
├── pyproject.toml              # Project configuration and dependencies
└── uv.lock                     # Dependency lock file
```

## Connect to Claude Desktop

### Option 1: Local Development (without Docker)

Add this configuration to your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "coxs-bazar-itinerary-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/code4mk/Documents/GitHub/gumpper-group/mcp-explore/mcp-server-python-template",
        "run",
        "cox-mcp-server"
      ]
    }
  }
}
```

### Option 2: Using Docker

First, build the Docker image:

```bash
docker build \
  --platform=linux/amd64 \
  --build-arg PYTHON_VERSION=3.12-slim \
  -t cox-mcp-server .
```

Then add this configuration to your Claude Desktop config file:

```json
{
  "mcpServers": {
    "coxs-bazar-itinerary-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "cox-mcp-server"
      ]
    }
  }
}
```

### Option 3: Using uvx (Run directly from GitHub)

Add this configuration to your Claude Desktop config file:

```json
{
  "mcpServers": {
    "coxs-bazar-itinerary-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/code4mk/coxs-bazar-itinerary-mcp-server.git",
        "cox-mcp-server"
      ]
    }
  }
}
```

## License

MIT