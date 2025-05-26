from mcp.models.context import ResourceContext

# Define available resources for cost analysis
COST_RESOURCES = {
    "cost_summary": ResourceContext(
        name="cost_summary",
        description="AWS cost summary data",
        type="json",
        required_params=["start_date", "end_date", "granularity"],
        optional_params=["group_by"]
    ),
    
    "service_costs": ResourceContext(
        name="service_costs",
        description="AWS costs broken down by service",
        type="json",
        required_params=["start_date", "end_date", "granularity"],
        optional_params=["top_n"]
    ),
    
    "account_costs": ResourceContext(
        name="account_costs",
        description="AWS costs broken down by account",
        type="json",
        required_params=["start_date", "end_date", "granularity"],
        optional_params=["top_n"]
    )
} 