from fredapi import Fred
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Any
from backend.database import get_session, store_series_data, get_series_data, FREDSeries, FREDData
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
        
    def _validate_api_key(self, api_key: Optional[str]) -> str:
        """Validate FRED API key format."""
        if not api_key:
            raise ValidationError("FRED API key is required")
        if not isinstance(api_key, str):
            raise ValidationError("FRED API key must be a string")
        if not re.match(r'^[a-f0-9]{32}$', api_key):
            raise ValidationError("Invalid FRED API key format")
        return api_key

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

    def _validate_series_data(self, series: pd.Series) -> None:
        """Validate series data for anomalies and continuity."""
        if series is None or series.empty:
            raise ValidationError("Empty or null series data")
        
        # Check for missing values
        if series.isnull().any():
            logger.warning(f"Series contains {series.isnull().sum()} missing values")
        
        # Check for extreme outliers (outside 3 standard deviations)
        mean = series.mean()
        std = series.std()
        outliers = series[abs(series - mean) > 3 * std]
        if not outliers.empty:
            logger.warning(f"Found {len(outliers)} outliers in series")

    @retry_on_failure(max_retries=3, delay=1)
    def fetch_and_store_historical_data(self):
        """Fetch and store complete historical data for all series with validation."""
        session = get_session()
        try:
            for series_id in SERIES_IDS.values():
                self._validate_series_id(series_id)
                logger.info(f"Fetching historical data for {series_id}")
                
                start_date = HISTORICAL_START_DATES.get(series_id)
                if start_date:
                    start_date = self._validate_date(start_date)
                
                # Get series data from FRED
                series = self.fred.get_series(
                    series_id,
                    observation_start=start_date
                )
                
                self._validate_series_data(series)
                
                # Get series metadata
                metadata = self.fred.get_series_info(series_id)
                if not metadata:
                    raise ValidationError(f"Failed to fetch metadata for series {series_id}")
                
                # Format and validate data points
                data_points = []
                for date, value in series.items():
                    try:
                        validated_value = self._validate_data_point(value)
                        validated_date = self._validate_date(date)
                        data_points.append({
                            'date': validated_date,
                            'value': validated_value
                        })
                    except ValidationError as e:
                        logger.warning(f"Skipping invalid data point: {str(e)}")
                        continue
                
                if not data_points:
                    raise ValidationError(f"No valid data points for series {series_id}")
                
                # Store in database
                store_series_data(session, series_id, data_points, metadata)
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
                
                # Fetch new data from FRED
                series = self.fred.get_series(
                    series_id,
                    observation_start=start_date
                )
                
                if series is None or series.empty:
                    logger.info(f"No new data for {series_id}")
                    continue
                
                self._validate_series_data(series)
                
                # Format and validate new data points
                data_points = []
                for date, value in series.items():
                    try:
                        validated_value = self._validate_data_point(value)
                        validated_date = self._validate_date(date)
                        data_points.append({
                            'date': validated_date,
                            'value': validated_value
                        })
                    except ValidationError as e:
                        logger.warning(f"Skipping invalid data point: {str(e)}")
                        continue
                
                if data_points:
                    metadata = self.fred.get_series_info(series_id)
                    if not metadata:
                        raise ValidationError(f"Failed to fetch metadata for series {series_id}")
                    store_series_data(session, series_id, data_points, metadata)
                    logger.info(f"Successfully updated data for {series_id}")
                
        except Exception as e:
            logger.error(f"Error updating daily data: {str(e)}")
            raise
        finally:
            session.close()

    @retry_on_failure(max_retries=3, delay=1)
    def get_inflation_metrics(self) -> Dict:
        """Fetch and process inflation-related data series with validation."""
        session = get_session()
        try:
            result_data = {}
            year_ago = datetime.now() - timedelta(days=365)
            
            for name, series_id in SERIES_IDS.items():
                self._validate_series_id(series_id)
                logger.info(f"Fetching data for {name} (series_id: {series_id})")
                
                try:
                    # Get series data from database
                    data_points = get_series_data(
                        session,
                        series_id,
                        start_date=year_ago
                    )
                    
                    if not data_points:
                        logger.warning(f"No data found for series {name} ({series_id})")
                        continue
                    
                    # Convert to pandas series for calculations
                    series = pd.Series(
                        [self._validate_data_point(point.value) for point in data_points],
                        index=[self._validate_date(point.date) for point in data_points]
                    )
                    
                    self._validate_series_data(series)
                    
                    baseline_value = float(series.iloc[0])
                    latest_value = float(series.iloc[-1])
                    
                    # Validate values are not zero to avoid division errors
                    if baseline_value == 0:
                        raise ValidationError(f"Baseline value is zero for series {name}")
                    
                    percentage_change = ((latest_value - baseline_value) / baseline_value) * 100
                    
                    # Get series metadata
                    series_info = session.query(FREDSeries)\
                        .filter_by(series_id=series_id)\
                        .first()
                    
                    if not series_info:
                        raise ValidationError(f"No metadata found for series {series_id}")
                    
                    # Format and validate historical data for charts
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
                        'current_value': latest_value,
                        'baseline_value': baseline_value,
                        'percentage_change': float(percentage_change),
                        'historical_data': historical_data,
                        'title': series_info.title,
                        'units': series_info.units,
                        'last_updated': series_info.last_updated.strftime('%Y-%m-%d')
                    }
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
