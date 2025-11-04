# Use Python slim image with configurable version
ARG PYTHON_VERSION=3.13-slim
FROM python:${PYTHON_VERSION}

# Set working directory
WORKDIR /app

# Install uv for faster dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files and README (required by hatchling build)
COPY pyproject.toml uv.lock README.md ./

# Copy source code
COPY src/ ./src/

# Install dependencies
RUN uv sync --frozen --no-dev

# Expose the port if needed (optional, MCP typically uses stdio)
# EXPOSE 8000

# Set the entrypoint to run the MCP server
ENTRYPOINT ["uv", "run", "cox-mcp-server"]

