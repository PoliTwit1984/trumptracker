from fredapi import Fred
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Any
from ..database import get_session, store_series_data, get_series_data, FREDSeries, FREDData
from .config import SERIES_IDS, HISTORICAL_START_DATES, get_fred_api_key
import re
from functools import wraps
import time
import numpy as np

logger = logging.getLogger(__name__)

def retry_on_failure(max_retries: int = 3, delay: int = 1):
    """Decorator to retry operations on failure with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        logger.error(f"Max retries ({max_retries}) reached for {func.__name__}")
                        raise
                    wait_time = delay * (2 ** (retries - 1))
                    logger.warning(f"Attempt {retries} failed for {func.__name__}. Retrying in {wait_time}s. Error: {str(e)}")
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class FREDDataFetcher:
    def __init__(self):
        """Initialize FRED API client with validation."""
        self.api_key = self._validate_api_key(get_fred_api_key())
        self.fred = Fred(api_key=self.api_key)
        logger.info("FRED API client initialized successfully")
        
    def _validate_api_key(self, api_key: Optional[str]) -> str:
        """Validate FRED API key."""
        if not api_key:
            raise ValidationError("FRED API key is required")
        if not isinstance(api_key, str):
            raise ValidationError("FRED API key must be a string")
        if len(api_key.strip()) == 0:
            raise ValidationError("FRED API key cannot be empty")
        return api_key.strip()

    def _validate_series_id(self, series_id: str) -> None:
        """Validate series ID."""
        if series_id not in SERIES_IDS.values():
            raise ValidationError(f"Invalid series ID: {series_id}")

    def _validate_date(self, date: Any) -> datetime:
        """Validate and parse date."""
        if isinstance(date, str):
            try:
                return datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise ValidationError(f"Invalid date format: {date}")
        elif isinstance(date, datetime):
            return date
        raise ValidationError(f"Invalid date type: {type(date)}")

    def _validate_data_point(self, value: Any) -> float:
        """Validate data point value."""
        try:
            value = float(value)
            if not np.isfinite(value):
                raise ValidationError(f"Invalid value: {value}")
            return value
        except (TypeError, ValueError):
            raise ValidationError(f"Invalid numeric value: {value}")

    def _validate_series_data(self, data_points: List) -> None:
        """Validate series data for anomalies and continuity."""
        if not data_points:
            raise ValidationError("Empty or null series data")
        
        # Convert to pandas series for validation
        series = pd.Series([point.value for point in data_points])
        
        # Check for missing values
        if series.isnull().any():
            logger.warning(f"Series contains {series.isnull().sum()} missing values")
        
        # Check for extreme outliers (outside 3 standard deviations)
        mean = series.mean()
        std = series.std()
        outliers = series[abs(series - mean) > 3 * std]
        if len(outliers) > 0:
            logger.warning(f"Found {len(outliers)} outliers in series")

    def get_inflation_metrics(self) -> Dict:
        """Fetch and process inflation-related data series from database."""
        session = get_session()
        try:
            result_data = {}
            year_ago = datetime.now() - timedelta(days=365)
            
            for name, series_id in SERIES_IDS.items():
                self._validate_series_id(series_id)
                logger.info(f"Fetching data for {name} (series_id: {series_id})")
                
                try:
                    # Get series data from database
                    logger.info(f"Querying database for series {series_id} from {year_ago}")
                    data_points = get_series_data(
                        session,
                        series_id,
                        start_date=year_ago
                    )
                    
                    if not data_points:
                        logger.warning(f"No data found in database for series {name} ({series_id})")
                        continue
                    
                    logger.info(f"Retrieved {len(data_points)} data points from database for {series_id}")
                    self._validate_series_data(data_points)
                    
                    # Get first and last data points
                    baseline_value = data_points[0].value
                    latest_value = data_points[-1].value
                    logger.info(f"Series {series_id} - Baseline: {baseline_value}, Latest: {latest_value}")
                    
                    # Validate values are not zero to avoid division errors
                    if baseline_value == 0:
                        raise ValidationError(f"Baseline value is zero for series {name}")
                    
                    percentage_change = ((latest_value - baseline_value) / baseline_value) * 100
                    logger.info(f"Series {series_id} - Percentage change: {percentage_change:.2f}%")
                    
                    # Get series metadata
                    series_info = session.query(FREDSeries)\
                        .filter_by(series_id=series_id)\
                        .first()
                    
                    if not series_info:
                        raise ValidationError(f"No metadata found in database for series {series_id}")
                    
                    logger.info(f"Retrieved metadata from database for series {series_id}")
                    
                    # Format historical data for charts
                    historical_data = []
                    for point in data_points:
                        try:
                            validated_value = self._validate_data_point(point.value)
                            validated_date = self._validate_date(point.date)
                            historical_data.append({
                                'date': validated_date.strftime('%Y-%m-%d'),
                                'value': validated_value
                            })
                        except ValidationError as e:
                            logger.warning(f"Skipping invalid historical data point: {str(e)}")
                            continue
                    
                    result_data[name] = {
                        'series_id': series_id,  # Include series_id in the result
                        'current_value': latest_value,
                        'baseline_value': baseline_value,
                        'percentage_change': float(percentage_change),
                        'historical_data': historical_data,
                        'title': series_info.title,
                        'units': series_info.units,
                        'last_updated': series_info.last_updated.strftime('%Y-%m-%d'),
                        'analysis': series_info.latest_analysis,
                        'analysis_timestamp': series_info.analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S') if series_info.analysis_timestamp else None
                    }
                    logger.info(f"Successfully processed data for series {series_id}")
                except Exception as e:
                    logger.error(f"Error processing series {name}: {str(e)}")
                    continue

            if not result_data:
                raise ValidationError("No valid data retrieved from database")

            return result_data

        except Exception as e:
            logger.error(f"Error processing inflation data: {str(e)}")
            raise
        finally:
            session.close()

    @retry_on_failure(max_retries=3, delay=1)
    def fetch_and_store_historical_data(self):
        """Fetch and store complete historical data for all series with validation."""
        session = get_session()
        try:
            # Set end_date to ensure we get the most recent data
            end_date = datetime.now() + timedelta(days=30)  # Look ahead to get any future releases
            
            for series_id in SERIES_IDS.values():
                self._validate_series_id(series_id)
                logger.info(f"Fetching historical data for {series_id}")
                
                start_date = HISTORICAL_START_DATES.get(series_id)
                if start_date:
                    start_date = self._validate_date(start_date)
                
                # Get series data from FRED with specific end date
                series = self.fred.get_series(
                    series_id,
                    observation_start=start_date,
                    observation_end=end_date
                )
                
                # Convert to list for validation
                data_points = [{'date': date, 'value': value} for date, value in series.items()]
                if not data_points:
                    raise ValidationError("Empty or null series data")
                
                # Get series metadata
                metadata = self.fred.get_series_info(series_id)
                if metadata is None or len(metadata) == 0:
                    raise ValidationError(f"Failed to fetch metadata for series {series_id}")
                
                # Format and validate data points
                validated_points = []
                for point in data_points:
                    try:
                        validated_value = self._validate_data_point(point['value'])
                        validated_date = self._validate_date(point['date'])
                        validated_points.append({
                            'date': validated_date,
                            'value': validated_value
                        })
                    except ValidationError as e:
                        logger.warning(f"Skipping invalid data point: {str(e)}")
                        continue
                
                if not validated_points:
                    raise ValidationError(f"No valid data points for series {series_id}")
                
                # Store in database
                store_series_data(session, series_id, validated_points, metadata)
                logger.info(f"Successfully stored historical data for {series_id}")
                
        except Exception as e:
            logger.error(f"Error fetching historical data: {str(e)}")
            raise
        finally:
            session.close()

    @retry_on_failure(max_retries=3, delay=1)
    def update_daily_data(self):
        """Check and update data for all series with validation."""
        session = get_session()
        try:
            # Set end_date to ensure we get the most recent data
            end_date = datetime.now() + timedelta(days=30)  # Look ahead to get any future releases
            
            for series_id in SERIES_IDS.values():
                self._validate_series_id(series_id)
                
                # Get latest data point from database
                latest = session.query(FREDData)\
                    .filter_by(series_id=series_id)\
                    .order_by(FREDData.date.desc())\
                    .first()
                
                if latest:
                    start_date = latest.date + timedelta(days=1)
                else:
                    start_date = self._validate_date(HISTORICAL_START_DATES.get(series_id))
                
                # Fetch new data from FRED with specific end date
                series = self.fred.get_series(
                    series_id,
                    observation_start=start_date,
                    observation_end=end_date
                )
                
                if series is None or len(series) == 0:
                    logger.info(f"No new data for {series_id}")
                    continue
                
                # Convert to list for validation
                data_points = [{'date': date, 'value': value} for date, value in series.items()]
                if not data_points:
                    continue
                
                # Format and validate new data points
                validated_points = []
                for point in data_points:
                    try:
                        validated_value = self._validate_data_point(point['value'])
                        validated_date = self._validate_date(point['date'])
                        validated_points.append({
                            'date': validated_date,
                            'value': validated_value
                        })
                    except ValidationError as e:
                        logger.warning(f"Skipping invalid data point: {str(e)}")
                        continue
                
                if validated_points:
                    metadata = self.fred.get_series_info(series_id)
                    if metadata is None or len(metadata) == 0:
                        raise ValidationError(f"Failed to fetch metadata for series {series_id}")
                    store_series_data(session, series_id, validated_points, metadata)
                    logger.info(f"Successfully updated data for {series_id}")
                
        except Exception as e:
            logger.error(f"Error updating daily data: {str(e)}")
            raise
        finally:
            session.close()
