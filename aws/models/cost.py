from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class CostSummaryRequest(BaseModel):
    """Request model for cost summary endpoint."""
    
    start_date: datetime = Field(..., description="Start date for cost analysis")
    end_date: datetime = Field(..., description="End date for cost analysis")
    granularity: str = Field(
        default="MONTHLY",
        description="Granularity of cost data (DAILY, MONTHLY, HOURLY)",
        pattern="^(DAILY|MONTHLY|HOURLY)$"
    )
    group_by: Optional[List[str]] = Field(
        default=["SERVICE"],
        description="Dimensions to group costs by (SERVICE, REGION, etc.)"
    )


class CostDataPoint(BaseModel):
    """Model for individual cost data points."""
    
    timestamp: datetime
    amount: float
    currency: str = "USD"
    service: Optional[str] = None
    region: Optional[str] = None
    usage_type: Optional[str] = None


class CostSummaryResponse(BaseModel):
    """Response model for cost summary endpoint."""
    
    total_cost: float
    currency: str = "USD"
    start_date: datetime
    end_date: datetime
    granularity: str
    cost_data: List[CostDataPoint]
    group_by: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_cost": 1234.56,
                "currency": "USD",
                "start_date": "2024-01-01T00:00:00Z",
                "end_date": "2024-01-31T23:59:59Z",
                "granularity": "MONTHLY",
                "cost_data": [
                    {
                        "timestamp": "2024-01-01T00:00:00Z",
                        "amount": 1234.56,
                        "currency": "USD",
                        "service": "Amazon EC2",
                        "region": "us-east-1"
                    }
                ],
                "group_by": ["SERVICE", "REGION"]
            }
        }
