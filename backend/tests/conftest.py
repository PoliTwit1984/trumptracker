import pytest
from unittest.mock import Mock, patch, MagicMock
import anthropic
import os

@pytest.fixture
def mock_fred_api_key():
    """Mock FRED API key."""
    with patch.dict('os.environ', {'FRED_API_KEY': '66e770a17fa10961986d08cf0ebbb556'}):
        yield '66e770a17fa10961986d08cf0ebbb556'

@pytest.fixture
def mock_anthropic_api_key():
    """Mock Anthropic API key."""
    with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test_key'}):
        yield 'test_key'

@pytest.fixture
def mock_anthropic():
    """Create a mock Anthropic client."""
    mock = MagicMock(spec=anthropic.Anthropic)
    mock.messages = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "Test analysis of inflation trends"
    mock.messages.create.return_value = mock_message
    return mock

@pytest.fixture
def sample_metrics():
    """Provide sample inflation metrics for testing."""
    return {
        'CPI': {
            'current_value': 314.69,
            'baseline_value': 308.02,
            'percentage_change': 2.50,
            'historical_data': [
                {'date': '2024-01-01', 'value': 308.02},
                {'date': '2024-02-01', 'value': 314.69}
            ],
            'title': 'Consumer Price Index',
            'units': 'Index 1982-1984=100',
            'last_updated': '2024-02-01'
        }
    }

@pytest.fixture
def mock_anthropic_response():
    """Create a mock Anthropic API response."""
    mock_response = Mock()
    mock_response.content = [Mock(text="Test analysis of inflation trends")]
    return mock_response

@pytest.fixture
def mock_api_error():
    """Create a mock API error."""
    return anthropic.APIError("Test API error")

@pytest.fixture
def mock_rate_limit_error():
    """Create a mock rate limit error."""
    return anthropic.RateLimitError("Rate limit exceeded")

@pytest.fixture
def mock_logger():
    """Create a mock logger."""
    with patch('logging.getLogger') as mock_get_logger:
        yield mock_get_logger

@pytest.fixture
def mock_claude_model():
    """Create a mock Claude model."""
    return 'claude-3-opus-20240229'

@pytest.fixture
def mock_retry_func():
    """Create a mock function for retry testing."""
    mock = Mock()
    mock.__name__ = 'mock_retry_func'
    return mock

@pytest.fixture
def mock_data_fetcher():
    """Create a mock data fetcher."""
    from backend.services.data_fetcher import FREDDataFetcher
    mock_fetcher = Mock(spec=FREDDataFetcher)
    mock_fetcher.get_inflation_metrics.return_value = {}
    return mock_fetcher

@pytest.fixture
def mock_data_analyzer():
    """Create a mock data analyzer."""
    from backend.services.data_analyzer import InflationAnalyzer
    mock_analyzer = Mock(spec=InflationAnalyzer)
    mock_analyzer.analyze_trends.return_value = "Test analysis"
    return mock_analyzer

@pytest.fixture
def mock_analysis_result():
    """Provide a mock analysis result."""
    return "Inflation trends show moderate growth with potential economic implications."

@pytest.fixture
def mock_fred_client():
    """Create a mock FRED client."""
    mock = Mock()
    mock.get_series.return_value = []
    mock.get_series_info.return_value = {'title': 'Test Series'}
    return mock

@pytest.fixture
def mock_session():
    """Create a mock database session."""
    mock = Mock()
    mock.query.return_value.filter_by.return_value.first.return_value = None
    return mock
