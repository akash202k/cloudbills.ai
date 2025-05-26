from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Optional
import logging

from aws.models.cost import CostSummaryRequest, CostSummaryResponse
from aws.services.cost_explorer import CostExplorerService
from aws.config import get_settings
import os

router = APIRouter()
logger = logging.getLogger(__name__)


async def verify_api_key(x_api_key: str = Header(...)):
    """Verify API key from request header."""
    settings = get_settings()
    # print(x_api_key)
    # print(os.environ['API_KEY'])
    if x_api_key != os.environ['API_KEY']:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return x_api_key


@router.post(
    "/cost-summary",
    response_model=CostSummaryResponse,
    # Comment out API key authentication dependency
    dependencies=[Depends(verify_api_key)]
)
async def get_cost_summary(request: CostSummaryRequest) -> CostSummaryResponse:
    """
    Get AWS cost summary for the specified time period.
    
    Args:
        request: CostSummaryRequest object containing query parameters
        
    Returns:
        CostSummaryResponse object with cost data
        
    Raises:
        HTTPException: If there's an error fetching cost data
    """
    try:
        cost_service = CostExplorerService()
        return cost_service.get_cost_summary(
            start_date=request.start_date,
            end_date=request.end_date,
            granularity=request.granularity,
            group_by=request.group_by
        )
    except Exception as e:
        logger.error(f"Error in get_cost_summary endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch cost data"
        )
