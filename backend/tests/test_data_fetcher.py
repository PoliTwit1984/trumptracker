import pytest
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
from backend.services.data_fetcher import (
    FREDDataFetcher,
    ValidationError,
    retry_on_failure
)

@pytest.fixture
def mock_fred():
    """Create a mock FRED API client."""
    with patch('fredapi.Fred') as mock:
        yield mock

@pytest.fixture
def mock_session():
    """Create a mock database session."""
    mock = Mock()
    with patch('backend.services.data_fetcher.get_session', return_value=mock):
        yield mock

@pytest.fixture
def data_fetcher(mock_fred, mock_fred_api_key):
    """Create a FREDDataFetcher instance with mocked dependencies."""
    return FREDDataFetcher()

def test_validate_api_key(data_fetcher):
    """Test API key validation."""
    # Test valid API key
    valid_key = "a" * 32
    assert data_fetcher._validate_api_key(valid_key) == valid_key
    
    # Test invalid API keys
    with pytest.raises(ValidationError):
        data_fetcher._validate_api_key(None)
    
    with pytest.raises(ValidationError):
        data_fetcher._validate_api_key(123)
    
    with pytest.raises(ValidationError):
        data_fetcher._validate_api_key("invalid_key")

def test_validate_series_id(data_fetcher):
    """Test series ID validation."""
    # Test valid series ID
    with patch('backend.services.data_fetcher.SERIES_IDS', {'test': 'TEST123'}):
        data_fetcher._validate_series_id('TEST123')
    
    # Test invalid series ID
    with pytest.raises(ValidationError):
        data_fetcher._validate_series_id('INVALID')

def test_validate_date(data_fetcher):
    """Test date validation."""
    # Test valid dates
    valid_date = datetime.now()
    assert data_fetcher._validate_date(valid_date) == valid_date
    
    valid_str = "2024-01-01"
    assert isinstance(data_fetcher._validate_date(valid_str), datetime)
    
    # Test invalid dates
    with pytest.raises(ValidationError):
        data_fetcher._validate_date("invalid_date")
    
    with pytest.raises(ValidationError):
        data_fetcher._validate_date(123)

def test_validate_data_point(data_fetcher):
    """Test data point validation."""
    # Test valid values
    assert data_fetcher._validate_data_point(123.45) == 123.45
    assert data_fetcher._validate_data_point("123.45") == 123.45
    
    # Test invalid values
    with pytest.raises(ValidationError):
        data_fetcher._validate_data_point("invalid")
    
    with pytest.raises(ValidationError):
        data_fetcher._validate_data_point(np.nan)
    
    with pytest.raises(ValidationError):
        data_fetcher._validate_data_point(np.inf)

def test_validate_series_data(data_fetcher):
    """Test series data validation."""
    # Test valid series
    valid_series = pd.Series([1.0, 2.0, 3.0])
    data_fetcher._validate_series_data(valid_series)
    
    # Test empty series
    with pytest.raises(ValidationError):
        data_fetcher._validate_series_data(pd.Series([]))
    
    # Test None
    with pytest.raises(ValidationError):
        data_fetcher._validate_series_data(None)

@pytest.mark.asyncio
async def test_fetch_and_store_historical_data(data_fetcher, mock_fred, mock_session):
    """Test fetching and storing historical data."""
    # Mock FRED API response
    mock_series = pd.Series([1.0, 2.0, 3.0], index=pd.date_range('2024-01-01', periods=3))
    mock_fred.return_value.get_series.return_value = mock_series
    mock_fred.return_value.get_series_info.return_value = {'title': 'Test Series'}
    
    # Test successful fetch and store
    data_fetcher.fetch_and_store_historical_data()
    
    # Verify API calls
    mock_fred.return_value.get_series.assert_called()
    mock_fred.return_value.get_series_info.assert_called()
    
    # Verify database calls
    mock_session.commit.assert_called()

@pytest.mark.asyncio
async def test_update_daily_data(data_fetcher, mock_fred, mock_session):
    """Test updating daily data."""
    # Mock database query
    mock_latest = Mock()
    mock_latest.date = datetime.now() - timedelta(days=1)
    mock_session.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = mock_latest
    
    # Mock FRED API response
    mock_series = pd.Series([4.0], index=[datetime.now()])
    mock_fred.return_value.get_series.return_value = mock_series
    mock_fred.return_value.get_series_info.return_value = {'title': 'Test Series'}
    
    # Test successful update
    data_fetcher.update_daily_data()
    
    # Verify API calls
    mock_fred.return_value.get_series.assert_called()
    mock_fred.return_value.get_series_info.assert_called()
    
    # Verify database calls
    mock_session.commit.assert_called()

def test_get_inflation_metrics(data_fetcher, mock_session):
    """Test getting inflation metrics."""
    # Mock database queries
    mock_data_points = [
        Mock(date=datetime.now() - timedelta(days=365), value=100.0),
        Mock(date=datetime.now(), value=102.0)
    ]
    mock_session.query.return_value.filter_by.return_value.first.return_value = Mock(
        title='Test Series',
        units='Index',
        last_updated=datetime.now()
    )
    
    with patch('backend.services.data_fetcher.get_series_data', return_value=mock_data_points):
        result = data_fetcher.get_inflation_metrics()
    
    # Verify result structure
    assert isinstance(result, dict)
    for metric in result.values():
        assert 'current_value' in metric
        assert 'baseline_value' in metric
        assert 'percentage_change' in metric
        assert 'historical_data' in metric
        assert 'title' in metric
        assert 'units' in metric
        assert 'last_updated' in metric

def test_retry_decorator(mock_retry_func):
    """Test retry decorator functionality."""
    # Set up mock function with side effects
    mock_retry_func.side_effect = [ValueError(), ValueError(), "success"]
    
    # Apply decorator
    decorated_func = retry_on_failure(max_retries=3, delay=0)(mock_retry_func)
    
    # Test successful retry
    result = decorated_func()
    assert result == "success"
    assert mock_retry_func.call_count == 3
    
    # Reset mock and test max retries exceeded
    mock_retry_func.reset_mock()
    mock_retry_func.side_effect = ValueError()
    
    with pytest.raises(ValueError):
        decorated_func()
    assert mock_retry_func.call_count == 3  # Should try 3 times before giving up
