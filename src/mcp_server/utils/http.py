from mcp_server.lib.httpx_client import HttpxClient

open_meteo_client = HttpxClient(
    base_url="https://api.open-meteo.com",
    mode="sync",
)

