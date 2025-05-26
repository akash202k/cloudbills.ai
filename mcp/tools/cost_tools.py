from mcp.models.context import ToolContext

# Define available tools for cost analysis
COST_TOOLS = {
    "get_cost_summary": ToolContext(
        name="get_cost_summary",
        description="Get AWS cost summary for a specified time period",
        parameters={
            "start_date": "Start date in YYYY-MM-DD format",
            "end_date": "End date in YYYY-MM-DD format",
            "granularity": "Time granularity (DAILY, MONTHLY, HOURLY)"
        },
        endpoint="/api/v1/costs/cost-summary",
        method="POST"
    ),
    
    "get_cost_by_service": ToolContext(
        name="get_cost_by_service",
        description="Get AWS costs broken down by service",
        parameters={
            "start_date": "Start date in YYYY-MM-DD format",
            "end_date": "End date in YYYY-MM-DD format",
            "granularity": "Time granularity (DAILY, MONTHLY, HOURLY)"
        },
        endpoint="/api/v1/costs/by-service",
        method="POST"
    ),
    
    "get_cost_by_account": ToolContext(
        name="get_cost_by_account",
        description="Get AWS costs broken down by account",
        parameters={
            "start_date": "Start date in YYYY-MM-DD format",
            "end_date": "End date in YYYY-MM-DD format",
            "granularity": "Time granularity (DAILY, MONTHLY, HOURLY)"
        },
        endpoint="/api/v1/costs/by-account",
        method="POST"
    )
} 