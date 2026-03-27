# Production Ready MCP Boilerplate

## Cox's Bazar AI Itinerary MCP Server

A Model Context Protocol (MCP) server that provides travel planning tools and weather information for Cox's Bazar, Bangladesh.

<a href="https://glama.ai/mcp/servers/@code4mk/coxs-bazar-itinerary-mcp-server">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@code4mk/coxs-bazar-itinerary-mcp-server/badge" alt="Cox's Bazar AI Itinerary Server MCP server" />
</a>

## Features

- **Weather Tools**: Get temperature forecasts and detailed weather information
- **Itinerary Tools**: Generate AI-powered travel itineraries
- **Travel Prompts**: Pre-configured prompts for travel planning

## Getting Started

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
This is serve the mcp server with auto-reload feature.

```bash
./scripts/run-mcp-server.sh
```


## Requirements
- Python 3.13+

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
│       ├── handlers/           # MCP handler registrations
│       │   ├── __init__.py
│       │   ├── tools/          # MCP tools
│       │   │   ├── __init__.py
│       │   │   ├── auth_additional.py  # Additional authentication tool
│       │   │   └── itinerary.py        # Travel itinerary tools
│       │   ├── resources/      # MCP resources
│       │   │   ├── __init__.py
│       │   │   └── weather.py      # Weather data resources
│       │   └── prompts/        # MCP prompts
│       │       ├── __init__.py
│       │       └── travel_prompts.py  # Travel planning prompts
│       ├── config/             # Configuration modules
│       │   ├── auth_provider.py    # Authentication provider
│       │   └── custom_routes.py    # Custom routes configuration
│       ├── services/           # Business logic
│       │   └── itenerary_service.py  # Itinerary business logic
│       ├── prompt_templates/   # Prompt text builders
│       │   ├── __init__.py
│       │   └── travel.py       # Travel prompt templates
│       └── utils/              # Utilities
│           ├── __init__.py
│           ├── elicitation.py  # Elicitation utilities
│           ├── get_weather_forecast.py  # Weather forecast utilities
│           └── helpers.py      # Helper functions
├── scripts/                    # Shell scripts
│   ├── run-inspector.sh        # Run MCP inspector
│   └── run-mcp-server.sh       # Run server script
├── tests/*                     # Test directory (unit, integration, fixtures)
├── _docs/*                     # Documentation files
├── Dockerfile                  # Docker configuration
├── glama.json                  # Glama configuration
├── pytest.ini                  # Pytest configuration
├── README.md                   # Project documentation
├── LICENSE                     # MIT License
├── pyproject.toml              # Project configuration and dependencies
└── uv.lock                     # Dependency lock file
```

## License

MIT