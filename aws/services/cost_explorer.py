import logging
from datetime import datetime
from typing import List, Dict, Any
import boto3
from botocore.exceptions import ClientError
from functools import lru_cache

from aws.models.cost import CostDataPoint, CostSummaryResponse
from aws.config import get_settings

logger = logging.getLogger(__name__)


class CostExplorerService:
    """Service for interacting with AWS Cost Explorer."""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = self._get_cost_explorer_client()
    
    def _get_cost_explorer_client(self):
        """Initialize and return AWS Cost Explorer client."""
        try:
            # If AWS profile is specified, use it
            if self.settings.AWS_PROFILE:
                session = boto3.Session(profile_name=self.settings.AWS_PROFILE)
                return session.client('ce', region_name=self.settings.AWS_REGION)
            
            # Otherwise, use explicit credentials if provided
            return boto3.client(
                'ce',
                aws_access_key_id=self.settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.settings.AWS_SECRET_ACCESS_KEY,
                region_name=self.settings.AWS_REGION
            )
        except Exception as e:
            logger.error(f"Failed to initialize Cost Explorer client: {str(e)}")
            raise
    
    def get_cost_summary(
        self,
        start_date: datetime,
        end_date: datetime,
        granularity: str,
        group_by: List[str]
    ) -> CostSummaryResponse:
        """
        Get cost summary from AWS Cost Explorer.
        
        Args:
            start_date: Start date for cost analysis
            end_date: End date for cost analysis
            granularity: Granularity of cost data
            group_by: Dimensions to group costs by
            
        Returns:
            CostSummaryResponse object with cost data
        """
        try:
            # Convert group_by list to tuple for caching
            group_by_tuple = tuple(sorted(group_by))
            
            # Get cached result if available
            cache_key = (start_date, end_date, granularity, group_by_tuple)
            cached_result = self._get_cached_cost_summary(*cache_key)
            if cached_result:
                return cached_result
            
            response = self.client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d')
                },
                Granularity=granularity,
                Metrics=['UnblendedCost'],
                GroupBy=[{'Type': 'DIMENSION', 'Key': key} for key in group_by]
            )
            
            cost_data = []
            total_cost = 0.0
            
            for result in response.get('ResultsByTime', []):
                for group in result.get('Groups', []):
                    amount = float(group['Metrics']['UnblendedCost']['Amount'])
                    total_cost += amount
                    
                    cost_data.append(
                        CostDataPoint(
                            timestamp=datetime.fromisoformat(result['TimePeriod']['Start']),
                            amount=amount,
                            currency=group['Metrics']['UnblendedCost']['Unit'],
                            service=group.get('Keys', [None])[0] if 'SERVICE' in group_by else None,
                            region=group.get('Keys', [None])[1] if 'REGION' in group_by else None
                        )
                    )
            
            result = CostSummaryResponse(
                total_cost=total_cost,
                start_date=start_date,
                end_date=end_date,
                granularity=granularity,
                cost_data=cost_data,
                group_by=group_by
            )
            
            # Cache the result
            self._cache_cost_summary(*cache_key, result)
            return result
            
        except ClientError as e:
            logger.error(f"AWS Cost Explorer API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_cost_summary: {str(e)}")
            raise
    
    @lru_cache(maxsize=100)
    def _get_cached_cost_summary(
        self,
        start_date: datetime,
        end_date: datetime,
        granularity: str,
        group_by_tuple: tuple
    ) -> CostSummaryResponse:
        """Get cached cost summary result."""
        return None
    
    def _cache_cost_summary(
        self,
        start_date: datetime,
        end_date: datetime,
        granularity: str,
        group_by_tuple: tuple,
        result: CostSummaryResponse
    ) -> None:
        """Cache cost summary result."""
        self._get_cached_cost_summary.cache_clear()  # Clear old cache
        self._get_cached_cost_summary(start_date, end_date, granularity, group_by_tuple)
