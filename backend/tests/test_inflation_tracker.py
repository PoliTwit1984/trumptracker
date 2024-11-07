"""Tests for the inflation tracking service."""

from unittest.mock import patch, MagicMock, create_autospec
import pytest
from datetime import datetime

from backend.services.inflation_tracker import InflationTracker
from backend.services.exceptions import ServiceInitializationError, DataProcessingError, BackupError
from backend.services.validators import validate_services, validate_response_format
from backend.services.data_fetcher import FREDDataFetcher
from backend.services.data_analyzer import InflationAnalyzer

@pytest.fixture
def mock_data_fetcher():
    """Create a mock data fetcher."""
    mock = MagicMock(spec=FREDDataFetcher)
    mock.__class__ = FREDDataFetcher
    return mock

@pytest.fixture
def mock_analyzer():
    """Create a mock analyzer."""
    mock = MagicMock(spec=InflationAnalyzer)
    mock.__class__ = InflationAnalyzer
    return mock

@pytest.fixture
def tracker(mock_data_fetcher, mock_analyzer):
    """Create an InflationTracker instance with mocked dependencies."""
    with patch('backend.services.inflation_tracker.FREDDataFetcher', return_value=mock_data_fetcher), \
         patch('backend.services.inflation_tracker.InflationAnalyzer', return_value=mock_analyzer):
        return InflationTracker()

def test_initialization_success(tracker):
    """Test successful initialization."""
    assert tracker.data_fetcher is not None
    assert tracker.analyzer is not None
    assert tracker.status is not None

def test_initialization_failure():
    """Test initialization failure."""
    with patch('backend.services.inflation_tracker.FREDDataFetcher', side_effect=Exception("Test error")), \
         pytest.raises(ServiceInitializationError):
        InflationTracker()

def test_validate_services(tracker):
    """Test service validation."""
    # Test with valid services
    validate_services(tracker.data_fetcher, tracker.analyzer)

    # Test with invalid services
    with pytest.raises(ServiceInitializationError):
        validate_services(None, tracker.analyzer)
    with pytest.raises(ServiceInitializationError):
        validate_services(tracker.data_fetcher, None)

def test_validate_response_format(tracker):
    """Test response format validation."""
    # Test valid format
    valid_data = {
        'status': 'Success',
        'last_updated': '2024-01-01',
        'metrics': {'CPI': {'value': 100}}
    }
    validate_response_format(valid_data)

    # Test invalid formats
    with pytest.raises(DataProcessingError):
        validate_response_format({'invalid': 'data'})
    with pytest.raises(DataProcessingError):
        validate_response_format({'status': 'Success'})
    with pytest.raises(DataProcessingError):
        validate_response_format({'status': 'Success', 'last_updated': '2024', 'metrics': 'invalid'})

def test_update_status(tracker):
    """Test status updates."""
    tracker._update_status('fetch', True)
    assert tracker.status['last_successful_fetch'] is not None

    tracker._update_status('analysis', False, 'Test error')
    assert len(tracker.status['errors']) == 1
    assert tracker.status['errors'][0]['operation'] == 'analysis'

def test_fetch_and_store_historical_data_success(tracker):
    """Test successful historical data fetch."""
    result = tracker.fetch_and_store_historical_data()
    assert result['status'] == 'Success'
    tracker.data_fetcher.fetch_and_store_historical_data.assert_called_once()

def test_fetch_and_store_historical_data_failure(tracker):
    """Test failed historical data fetch."""
    tracker.data_fetcher.fetch_and_store_historical_data.side_effect = Exception("Test error")
    with pytest.raises(DataProcessingError):
        tracker.fetch_and_store_historical_data()

def test_update_daily_data_success(tracker):
    """Test successful daily data update."""
    result = tracker.update_daily_data()
    assert result['status'] == 'Success'
    tracker.data_fetcher.update_daily_data.assert_called_once()

def test_update_daily_data_failure(tracker):
    """Test failed daily data update."""
    tracker.data_fetcher.update_daily_data.side_effect = Exception("Test error")
    with pytest.raises(DataProcessingError):
        tracker.update_daily_data()

def test_get_inflation_data_success(tracker):
    """Test successful inflation data retrieval."""
    tracker.data_fetcher.get_inflation_metrics.return_value = {'CPI': {'value': 100}}
    tracker.analyzer.analyze_trends.return_value = 'Test analysis'
    
    result = tracker.get_inflation_data()
    assert result['status'] == 'Success'
    assert 'metrics' in result
    assert 'analysis' in result

def test_get_inflation_data_fetch_failure(tracker):
    """Test inflation data fetch failure."""
    tracker.data_fetcher.get_inflation_metrics.side_effect = Exception("Test error")
    
    result = tracker.get_inflation_data()
    assert result['status'] == 'Error'
    assert 'error' in result

def test_get_inflation_data_analysis_failure(tracker):
    """Test inflation data analysis failure."""
    tracker.data_fetcher.get_inflation_metrics.return_value = {'CPI': {'value': 100}}
    tracker.analyzer.analyze_trends.side_effect = Exception("Test error")
    
    result = tracker.get_inflation_data()
    assert result['status'] == 'Error'
    assert 'error' in result

def test_backup_data_success(tracker):
    """Test successful data backup."""
    with patch('backend.services.inflation_tracker.backup_database', return_value=True):
        result = tracker.backup_data()
        assert result['status'] == 'Success'

def test_backup_data_failure(tracker):
    """Test failed data backup."""
    with patch('backend.services.inflation_tracker.backup_database', return_value=False), \
         pytest.raises(BackupError):
        tracker.backup_data()

def test_get_status(tracker):
    """Test status retrieval."""
    tracker._update_status('fetch', True)
    tracker._update_status('analysis', False, 'Test error')
    
    status = tracker.get_status()
    assert status['status'] == 'Success'
    assert 'operations' in status
    assert 'recent_errors' in status
    assert len(status['recent_errors']) == 1

def test_retry_mechanism(tracker):
    """Test retry mechanism for operations."""
    # Set up mock to fail twice then succeed
    mock_operation = MagicMock(side_effect=[
        Exception("First failure"),
        Exception("Second failure"),
        {'status': 'Success'}
    ])
    
    tracker.data_fetcher.fetch_and_store_historical_data = mock_operation
    result = tracker.fetch_and_store_historical_data()
    
    assert result['status'] == 'Success'
    assert mock_operation.call_count == 3
