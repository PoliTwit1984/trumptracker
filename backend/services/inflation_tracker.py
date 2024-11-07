"""Main inflation tracking service."""

from datetime import datetime
import logging
from typing import Dict, Union, Optional

from .data_fetcher import FREDDataFetcher
from .data_analyzer import InflationAnalyzer
from .exceptions import ServiceInitializationError, DataProcessingError, BackupError
from .decorators import retry_on_failure
from .validators import validate_services, validate_response_format
from backend.database import backup_database

logger = logging.getLogger(__name__)

class InflationTracker:
    def __init__(self):
        """Initialize FRED data fetcher and inflation analyzer with validation."""
        try:
            self.data_fetcher = FREDDataFetcher()
            self.analyzer = InflationAnalyzer()
            validate_services(self.data_fetcher, self.analyzer)
            self.status = {
                'last_successful_fetch': None,
                'last_successful_analysis': None,
                'last_successful_backup': None,
                'errors': []
            }
        except Exception as e:
            raise ServiceInitializationError(f"Failed to initialize services: {str(e)}")

    def _update_status(self, operation: str, success: bool, error: Optional[str] = None) -> None:
        """Update tracker status."""
        current_time = datetime.now().isoformat()
        if success:
            self.status[f'last_successful_{operation}'] = current_time
        if error:
            self.status['errors'].append({
                'timestamp': current_time,
                'operation': operation,
                'error': error
            })
            # Keep only last 100 errors
            self.status['errors'] = self.status['errors'][-100:]

    @retry_on_failure(max_retries=3, delay=1)
    def fetch_and_store_historical_data(self) -> Dict[str, str]:
        """Fetch and store complete historical data for all series with validation."""
        try:
            self.data_fetcher.fetch_and_store_historical_data()
            self._update_status('fetch', True)
            return {
                'status': 'Success',
                'message': 'Historical data fetched and stored successfully'
            }
        except Exception as e:
            error_msg = f"Error fetching historical data: {str(e)}"
            self._update_status('fetch', False, error_msg)
            raise DataProcessingError(error_msg)

    @retry_on_failure(max_retries=3, delay=1)
    def update_daily_data(self) -> Dict[str, str]:
        """Check and update data for all series with validation."""
        try:
            self.data_fetcher.update_daily_data()
            self._update_status('fetch', True)
            return {
                'status': 'Success',
                'message': 'Daily data updated successfully'
            }
        except Exception as e:
            error_msg = f"Error updating daily data: {str(e)}"
            self._update_status('fetch', False, error_msg)
            raise DataProcessingError(error_msg)

    def get_inflation_data(self) -> Dict[str, Union[dict, str]]:
        """
        Fetch and process inflation-related data series with comprehensive validation.
        Returns formatted data for frontend consumption.
        """
        try:
            # Get metrics data
            result_data = self.data_fetcher.get_inflation_metrics()
            self._update_status('fetch', True)

            # Get AI analysis of the trends
            logger.info("Getting AI analysis of trends")
            analysis = self.analyzer.analyze_trends(result_data)
            self._update_status('analysis', True)

            response = {
                'status': 'Success',
                'last_updated': datetime.now().strftime('%Y-%m-%d'),
                'metrics': result_data,
                'analysis': analysis
            }

            # Validate response format
            validate_response_format(response)
            return response

        except Exception as e:
            error_msg = f"Error processing inflation data: {str(e)}"
            logger.error(error_msg)
            self._update_status('fetch', False, error_msg)
            return {
                'status': 'Error',
                'error': error_msg,
                'last_updated': datetime.now().strftime('%Y-%m-%d')
            }

    @retry_on_failure(max_retries=3, delay=1)
    def backup_data(self) -> Dict[str, str]:
        """Create a backup of the database with validation."""
        try:
            success = backup_database()
            if not success:
                raise BackupError("Backup operation failed")
            
            self._update_status('backup', True)
            return {
                'status': 'Success',
                'message': 'Database backup completed successfully'
            }
        except Exception as e:
            error_msg = f"Error during database backup: {str(e)}"
            self._update_status('backup', False, error_msg)
            raise BackupError(error_msg)

    def get_status(self) -> Dict:
        """Get current tracker status."""
        return {
            'status': 'Success',
            'last_updated': datetime.now().strftime('%Y-%m-%d'),
            'operations': {
                key: value for key, value in self.status.items()
                if key != 'errors'
            },
            'recent_errors': self.status['errors'][-5:] if self.status['errors'] else []
        }
