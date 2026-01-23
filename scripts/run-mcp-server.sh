uv run watchmedo auto-restart \
  --directory="src" \
  --patterns="*.py" \
  --recursive \
  -- uv run mcp-server
