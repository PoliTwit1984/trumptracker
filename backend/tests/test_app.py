import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from backend.app import app, validate_client, fred_client
from backend.services.inflation_tracker import ServiceInitializationError

@pytest.fixture
def client():
    """Create a test client."""
    app.config['TESTING'] = True
    app.config['RATELIMIT_ENABLED'] = True
    app.config['RATELIMIT_STORAGE_URL'] = 'memory://'
    with app.test_client() as client:
        yield client

def test_environment_validation():
    """Test environment variable validation."""
    with patch.dict('os.environ', {'FRED_API_KEY': '', 'ANTHROPIC_API_KEY': ''}):
        with pytest.raises(Exception):
            validate_environment()

def test_client_validation():
    """Test FRED client validation."""
    # Test with no client
    with patch('backend.app.fred_client', None):
        with pytest.raises(ServiceInitializationError, match='FRED client not initialized'):
            validate_client()

def test_security_headers(client):
    """Test security headers are set."""
    response = client.get('/api/v1/health')
    headers = response.headers
    
    assert headers['X-Content-Type-Options'] == 'nosniff'
    assert headers['X-Frame-Options'] == 'DENY'
    assert headers['X-XSS-Protection'] == '1; mode=block'
    assert 'max-age=31536000' in headers['Strict-Transport-Security']

def test_health_check_healthy(client, mock_fred_client):
    """Test health check endpoint when healthy."""
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert 'version' in data
    assert 'services' in data

def test_health_check_unhealthy(client):
    """Test health check endpoint when unhealthy."""
    with patch('backend.app.fred_client', None):
        response = client.get('/api/v1/health')
        assert response.status_code == 503
        data = response.get_json()
        assert data['status'] == 'unhealthy'
        assert 'timestamp' in data
        assert 'error' in data

def test_initialize_data_success(client, mock_fred_client):
    """Test successful data initialization."""
    mock_fred_client.fetch_and_store_historical_data.return_value = {
        'status': 'Success',
        'message': 'Data initialized'
    }
    
    response = client.post('/api/v1/inflation/initialize')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'Success'

def test_initialize_data_failure(client, mock_fred_client):
    """Test failed data initialization."""
    mock_fred_client.fetch_and_store_historical_data.side_effect = Exception('Test error')
    
    response = client.post('/api/v1/inflation/initialize')
    assert response.status_code == 500
    data = response.get_json()
    assert data['status'] == 'Error'

def test_update_data_success(client, mock_fred_client):
    """Test successful data update."""
    mock_fred_client.update_daily_data.return_value = {
        'status': 'Success',
        'message': 'Data updated'
    }
    
    response = client.post('/api/v1/inflation/update')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'Success'

def test_update_data_failure(client, mock_fred_client):
    """Test failed data update."""
    mock_fred_client.update_daily_data.side_effect = Exception('Test error')
    
    response = client.post('/api/v1/inflation/update')
    assert response.status_code == 500
    data = response.get_json()
    assert data['status'] == 'Error'

def test_backup_data_success(client, mock_fred_client):
    """Test successful data backup."""
    mock_fred_client.backup_data.return_value = {
        'status': 'Success',
        'message': 'Backup completed'
    }
    
    response = client.post('/api/v1/inflation/backup')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'Success'

def test_backup_data_failure(client, mock_fred_client):
    """Test failed data backup."""
    mock_fred_client.backup_data.side_effect = Exception('Test error')
    
    response = client.post('/api/v1/inflation/backup')
    assert response.status_code == 500
    data = response.get_json()
    assert data['status'] == 'Error'

def test_get_inflation_data_success(client, mock_fred_client):
    """Test successful inflation data retrieval."""
    mock_fred_client.get_inflation_data.return_value = {
        'status': 'Success',
        'metrics': {},
        'analysis': 'Test analysis'
    }
    
    response = client.get('/api/v1/inflation/data')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'Success'

def test_get_inflation_data_failure(client, mock_fred_client):
    """Test failed inflation data retrieval."""
    mock_fred_client.get_inflation_data.side_effect = Exception('Test error')
    
    response = client.get('/api/v1/inflation/data')
    assert response.status_code == 500
    data = response.get_json()
    assert data['status'] == 'Error'

def test_rate_limiting(client, mock_fred_client):
    """Test rate limiting functionality."""
    # First request should succeed
    response = client.get('/api/v1/inflation/data')
    assert response.status_code == 200

    # Second request within the limit window should be rate limited
    response = client.get('/api/v1/inflation/data')
    assert response.status_code == 429
    data = response.get_json()
    assert data['error'] == 'Rate limit exceeded'

def test_error_handling(client, mock_fred_client):
    """Test error handling middleware."""
    mock_fred_client.get_inflation_data.side_effect = ValueError('Test error')
    
    response = client.get('/api/v1/inflation/data')
    assert response.status_code == 500
    data = response.get_json()
    assert data['status'] == 'Error'
    assert 'timestamp' in data

def test_request_logging(client, mock_fred_client, mock_logger):
    """Test request logging."""
    client.get('/api/v1/inflation/data')
    mock_logger.info.assert_called()
