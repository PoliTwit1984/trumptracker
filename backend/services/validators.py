"""Validators for the inflation tracking service."""

from typing import Dict
from .exceptions import ServiceInitializationError, DataProcessingError
from .data_fetcher import FREDDataFetcher
from .data_analyzer import InflationAnalyzer

def validate_services(data_fetcher: FREDDataFetcher, analyzer: InflationAnalyzer) -> None:
    """Validate that required services are properly initialized."""
    if not isinstance(data_fetcher, FREDDataFetcher):
        raise ServiceInitializationError("Invalid data fetcher service")
    if not isinstance(analyzer, InflationAnalyzer):
        raise ServiceInitializationError("Invalid analyzer service")

def validate_response_format(data: Dict) -> None:
    """Validate response data format."""
    required_fields = {'status', 'last_updated'}
    if not isinstance(data, dict):
        raise DataProcessingError("Response must be a dictionary")
    if not all(field in data for field in required_fields):
        missing_fields = required_fields - set(data.keys())
        raise DataProcessingError(f"Missing required fields: {missing_fields}")
    
    if 'metrics' in data:
        if not isinstance(data['metrics'], dict):
            raise DataProcessingError("Metrics must be a dictionary")
        for metric_name, metric_data in data['metrics'].items():
            if not isinstance(metric_data, dict):
                raise DataProcessingError(f"Invalid metric data format for {metric_name}")
