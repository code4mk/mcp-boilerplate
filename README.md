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

### Run with MCP dev (development) - inspector tool

* Need node version > 20.x.x

```bash
uv run mcp dev src/mcp_server/server.py
```

### Run as installed command
```bash
uv run cox-mcp-server
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
│       ├── tools/              # MCP tools
│       │   ├── __init__.py
│       │   └── itinerary.py    # Travel itinerary tools
│       ├── resources/          # MCP resources
│       │   ├── __init__.py
│       │   └── weather.py      # Weather data resources
│       ├── prompts/            # MCP prompts
│       │   ├── __init__.py
│       │   └── travel_prompts.py  # Travel planning prompts
│       └── utils/              # Utilities
│           ├── __init__.py
│           ├── helpers.py      # Helper functions
│           └── register_mcp_components.py  # MCP component registration
├── tests/                      # Test directory
├── Dockerfile                  # Docker configuration
├── .dockerignore               # Docker ignore file
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