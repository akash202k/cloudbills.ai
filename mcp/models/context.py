from typing import Dict, List, Optional
from pydantic import BaseModel


class BackendContext(BaseModel):
    """Context model for backend API interactions."""
    base_url: str = "http://localhost:8000"
    api_version: str = "v1"
    endpoints: Dict[str, str] = {
        "cost_summary": "/api/v1/costs/cost-summary",
        "health": "/health"
    }


class ToolContext(BaseModel):
    """Context model for tool definitions."""
    name: str
    description: str
    parameters: Dict[str, str]
    endpoint: str
    method: str = "POST"


class ResourceContext(BaseModel):
    """Context model for resource definitions."""
    name: str
    description: str
    type: str
    required_params: List[str]
    optional_params: Optional[List[str]] = None 