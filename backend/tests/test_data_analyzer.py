import pytest
from unittest.mock import Mock, patch
from datetime import datetime
import anthropic
from backend.services.data_analyzer import (
    InflationAnalyzer,
    AnalyzerError,
    ValidationError,
    PromptError,
    APIError
)

@pytest.fixture
def analyzer(mock_anthropic, mock_claude_model):
    """Create an InflationAnalyzer instance with mocked dependencies."""
    return InflationAnalyzer()

def test_validate_model(analyzer):
    """Test model name validation."""
    # Test valid model
    assert analyzer._validate_model('claude-3-opus-20240229') == 'claude-3-opus-20240229'
    
    # Test invalid models
    with pytest.raises(ValidationError):
        analyzer._validate_model(None)
    
    with pytest.raises(ValidationError):
        analyzer._validate_model('')
    
    with pytest.raises(ValidationError):
        analyzer._validate_model('invalid-model')

def test_validate_metrics(analyzer, sample_metrics):
    """Test metrics data validation."""
    # Test valid metrics
    analyzer._validate_metrics(sample_metrics)
    
    # Test invalid metrics structure
    with pytest.raises(ValidationError):
        analyzer._validate_metrics(None)
    
    with pytest.raises(ValidationError):
        analyzer._validate_metrics([])
    
    # Test missing required fields
    invalid_metrics = {
        'CPI': {
            'title': 'Consumer Price Index'
            # Missing other required fields
        }
    }
    with pytest.raises(ValidationError):
        analyzer._validate_metrics(invalid_metrics)
    
    # Test invalid numeric fields
    invalid_metrics = {
        'CPI': {
            **sample_metrics['CPI'],
            'percentage_change': 'invalid'
        }
    }
    with pytest.raises(ValidationError):
        analyzer._validate_metrics(invalid_metrics)
    
    # Test invalid historical data
    invalid_metrics = {
        'CPI': {
            **sample_metrics['CPI'],
            'historical_data': [{'invalid': 'data'}]
        }
    }
    with pytest.raises(ValidationError):
        analyzer._validate_metrics(invalid_metrics)

def test_validate_prompt(analyzer):
    """Test prompt validation."""
    # Test valid prompt
    valid_prompt = "Test prompt with sufficient length and content about inflation metrics"
    analyzer._validate_prompt(valid_prompt)
    
    # Test invalid prompts
    with pytest.raises(PromptError):
        analyzer._validate_prompt(None)
    
    with pytest.raises(PromptError):
        analyzer._validate_prompt("")
    
    # Test prompt length limit
    long_prompt = "x" * 5000
    with pytest.raises(PromptError):
        analyzer._validate_prompt(long_prompt)

def test_validate_analysis_output(analyzer):
    """Test analysis output validation."""
    # Test valid analysis
    valid_analysis = """
    The current state of inflation shows moderate increases.
    Key changes include rising consumer prices and housing costs.
    These trends imply potential economic impacts going forward.
    """
    assert analyzer._validate_analysis_output(valid_analysis) is True
    
    # Test invalid analysis
    assert analyzer._validate_analysis_output("") is False
    assert analyzer._validate_analysis_output("Too short") is False
    assert analyzer._validate_analysis_output("No analysis components") is False

def test_prepare_analysis_prompt(analyzer, sample_metrics):
    """Test analysis prompt preparation."""
    # Test valid prompt generation
    prompt = analyzer._prepare_analysis_prompt(sample_metrics)
    assert isinstance(prompt, str)
    assert len(prompt) > 0
    assert "Consumer Price Index" in prompt
    assert "2.50%" in prompt  # Fixed to match the exact format
    
    # Test empty metrics
    with pytest.raises(PromptError):
        analyzer._prepare_analysis_prompt({})

@pytest.mark.asyncio
async def test_analyze_trends_success(analyzer, mock_anthropic, sample_metrics, mock_anthropic_response):
    """Test successful trend analysis."""
    # Mock Anthropic API response
    mock_anthropic.return_value.messages.create.return_value = mock_anthropic_response
    
    # Test successful analysis
    result = analyzer.analyze_trends(sample_metrics)
    assert isinstance(result, str)
    assert len(result) > 0
    
    # Verify API call
    mock_anthropic.return_value.messages.create.assert_called_once()

@pytest.mark.asyncio
async def test_analyze_trends_api_error(analyzer, mock_anthropic, sample_metrics, mock_api_error):
    """Test handling of API errors."""
    # Mock API error
    mock_anthropic.return_value.messages.create.side_effect = mock_api_error
    
    # Test error handling
    result = analyzer.analyze_trends(sample_metrics)
    assert "Unable to analyze trends" in result

def test_retry_mechanism(analyzer, mock_anthropic, sample_metrics):
    """Test retry mechanism for API calls."""
    # Mock API calls with failures then success
    mock_response = Mock()
    mock_response.content = "Analysis after retry"
    mock_anthropic.return_value.messages.create.side_effect = [
        Exception("First failure"),
        Exception("Second failure"),
        mock_response
    ]
    
    # Test retry behavior
    result = analyzer.analyze_trends(sample_metrics)
    assert isinstance(result, str)
    assert result == "Analysis after retry"
    assert mock_anthropic.return_value.messages.create.call_count == 3

def test_rate_limit_handling(analyzer, mock_anthropic, sample_metrics, mock_rate_limit_error):
    """Test handling of rate limits."""
    mock_anthropic.return_value.messages.create.side_effect = mock_rate_limit_error
    
    result = analyzer.analyze_trends(sample_metrics)
    assert "Rate limit exceeded" in result
    assert "Unable to analyze trends" in result

def test_error_logging(analyzer, mock_anthropic, sample_metrics, mock_logger):
    """Test error logging functionality."""
    # Mock API error
    test_error = "Test error"
    mock_anthropic.return_value.messages.create.side_effect = Exception(test_error)
    
    # Configure logger mock
    error_logger = Mock()
    mock_logger.return_value = error_logger
    
    # Test error logging
    analyzer.analyze_trends(sample_metrics)
    
    # Verify error was logged
    error_logger.error.assert_called_with(f"Unexpected error analyzing trends: {test_error}")
