
from fastmcp import Context
from mcp_server.mcp_instance import mcp
from mcp_server.core.services.itenerary_service import s_generate_itinerary, s_get_activity_suggestions
from mcp_server.models.itinerary_models import GenerateItinerarySchema, GetActivitySuggestionsSchema

@mcp.tool(
    name="generate_itinerary",
    description="generate itinerary for coxs bazar",
)
async def generate_itinerary(
    ctx: Context,
    params: GenerateItinerarySchema
) -> str:
    """ Generate itinerary for coxs bazar
    Args:
        ctx: FastMCP Context
        params: GenerateItinerarySchema: Parameters for generating an itinerary
    Returns:
        str: Itinerary for coxs bazar
    """
    output = await s_generate_itinerary(ctx, params.start_date, params.days)
    return output

@mcp.tool(
    name="get_activity_suggestions",
    description="suggest activities based on temperature and time of day",
)
async def get_activity_suggestions(
    ctx: Context,
    params: GetActivitySuggestionsSchema
) -> list[str]:
    """
    Suggest activities based on temperature and time of day
    Args:
        ctx: FastMCP Context
        params: GetActivitySuggestionsSchema: Parameters for getting activity suggestions
    Returns:
        list[str]: List of suggested activities
    """
    return await s_get_activity_suggestions(params.temperature, params.time_of_day)
