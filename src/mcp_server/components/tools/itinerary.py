"""Itinerary generation tools."""
from datetime import datetime
from dateutil import parser
from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from mcp_server.models import ItineraryPreferences

def register_itinerary_tools(mcp):
    """Register itinerary tools with the MCP server."""
    
    @mcp.tool()
    async def cox_ai_itinerary(days: int, start_date: str, ctx: Context[ServerSession, None]) -> str:
        """
        Full workflow: fetch daily temperatures + generate AI itinerary.
        Uses the registered MCP prompt 'generate_itinerary' for consistency.
        
        Args:
            days: Number of days for the trip
            start_date: Start date (e.g., "2025-01-15", "15 Jan 2025", "today")
        
        Returns:
            Formatted prompt for AI to generate detailed itinerary
        """
        from mcp_server.components.resources.weather import get_temperature_forecast
        from mcp_server.components.prompts.travel_prompts import get_prompt
        
        elicitation_note = ""  # To store any warnings about client capabilities
        
        # Elicitation: Suggest minimum 2 days for a better itinerary
        if days == 1:
            try:
                print("Elicitation: Suggest minimum 2 days for a better itinerary")
                result = await ctx.elicit(
                    message=(
                        f"⚠️ Only 1 day detected for your itinerary starting on {start_date}! "
                        "For a meaningful travel experience, we recommend at least 2 days. "
                        "This allows for varied activities, proper rest, and a better exploration of the destination. "
                        "Would you like to extend your trip to 2 or more days?"
                    ),
                    schema=ItineraryPreferences,
                )
                
                if result.action == "accept" and result.data:
                    if result.data.extendTrip:
                        # Use the new extended days
                        days = max(result.data.newDays, 2)  # Ensure at least 2 days
                    else:
                        return "[CANCELLED] Itinerary generation cancelled. Please plan for at least 2 days for a better experience."
                else:
                    return "[CANCELLED] Itinerary generation cancelled by user."
            except (AttributeError, NotImplementedError, Exception) as e:
                # If elicitation is not supported by the client, continue with 1 day
                # but add a warning message to the output
                print(f"Note: Elicitation not supported by client ({type(e).__name__}). Proceeding with 1-day itinerary.")
                elicitation_note = (
                    "ℹ️ NOTE: Your MCP client does not support interactive elicitation. "
                    "We recommend at least 2 days for a better travel experience. "
                    "Proceeding with 1-day itinerary. and very last add the note that this client does not support interactive elicitation\n\n"
                )
        
        # Parse start date
        try:
            start_dt = parser.parse(start_date)
        except Exception:
            start_dt = datetime.today()
        
        # Get temperature forecast
        temp_list = get_temperature_forecast(start_dt, days)
        
        # Use the MCP prompt for generating itinerary
        generate_itinerary_prompt = get_prompt('generate_itinerary')
        if generate_itinerary_prompt:
            itinerary_result = generate_itinerary_prompt(days, temp_list, start_date)
            return elicitation_note + itinerary_result
        
        # Fallback if prompt not found
        return elicitation_note + "Error: Could not load itinerary prompt"
    
    @mcp.tool()
    def get_activity_suggestions(temperature: float, time_of_day: str = "afternoon"):
        """
        Suggest activities based on temperature and time of day.
        
        Args:
            temperature: Temperature in Celsius
            time_of_day: "morning", "afternoon", or "evening"
        
        Returns:
            List of suggested activities
        """
        activities = []
        
        # Temperature-based activities
        if temperature < 25:
            activities.extend([
                "Beach walk and photography",
                "Visit Himchari National Park",
                "Explore local markets",
            ])
        elif temperature < 30:
            activities.extend([
                "Swimming at Inani Beach",
                "Visit Marine Drive",
                "Surfing lessons",
                "Jet skiing",
            ])
        else:  # Hot day
            activities.extend([
                "Visit Aggmeda Khyang (Buddhist monastery)",
                "Indoor shopping at malls",
                "Enjoy fresh coconut water by the beach",
                "Take a boat ride",
            ])
        
        # Time-specific activities
        if time_of_day == "morning":
            activities.extend([
                "Sunrise at Laboni Beach",
                "Fresh seafood breakfast",
                "Bird watching at wetlands",
            ])
        elif time_of_day == "afternoon":
            activities.extend([
                "Lunch at beach restaurants",
                "Visit Ramu Buddhist Temple",
                "Shopping for local handicrafts",
            ])
        else:  # evening
            activities.extend([
                "Sunset at Cox's Bazar beach",
                "Dinner with sea view",
                "Night market exploration",
                "Beach bonfire (if available)",
            ])
        
        return activities