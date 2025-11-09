from mcp_server.mcp_instance import mcp
from mcp_server.core.prompts.travel import get_itinerary_prompt

@mcp.prompt()
async def generate_itinerary_prompt(days: int, start_date: str) -> str:
    return await get_itinerary_prompt(days, start_date)
