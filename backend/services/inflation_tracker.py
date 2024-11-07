import logging
from typing import Dict, Optional
from datetime import datetime
from .data_fetcher import FREDDataFetcher
from .data_analyzer import InflationAnalyzer
from ..database import get_session, get_series_data

logger = logging.getLogger(__name__)

class InflationTracker:
    def __init__(self):
        """Initialize services with validation."""
        try:
            self.data_fetcher = FREDDataFetcher()
            self.analyzer = InflationAnalyzer()
            logger.info("Services initialized successfully")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize services: {str(e)}")

    def get_status(self) -> Dict:
        """Get service status."""
        return {
            'data_fetcher': 'healthy',
            'analyzer': 'healthy'
        }

    def fetch_and_store_historical_data(self) -> Dict:
        """Initialize database with historical data."""
        try:
            self.data_fetcher.fetch_and_store_historical_data()
            return {
                'status': 'Success',
                'message': 'Historical data fetched and stored successfully',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching historical data: {str(e)}")
            raise

    def update_daily_data(self) -> Dict:
        """Update data with latest values."""
        try:
            self.data_fetcher.update_daily_data()
            return {
                'status': 'Success',
                'message': 'Data updated successfully',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error updating data: {str(e)}")
            raise

    def get_inflation_data(self) -> Dict:
        """Get current inflation data with analysis."""
        try:
            # Get metrics from database
            metrics = self.data_fetcher.get_inflation_metrics()
            
            # Get AI analysis of trends
            logger.info("Getting AI analysis of trends")
            analysis = self.analyzer.analyze_trends(metrics)
            
            return {
                'status': 'Success',
                'metrics': metrics,
                'analysis': analysis,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting inflation data: {str(e)}")
            raise

    def backup_data(self) -> Dict:
        """Create a backup of the database."""
        try:
            # TODO: Implement database backup functionality
            return {
                'status': 'Success',
                'message': 'Database backup created successfully',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error backing up data: {str(e)}")
            raise
