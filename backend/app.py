from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import time
from typing import Dict, Any, Tuple
from functools import wraps
import traceback

# Configure logging first
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ConfigurationError(Exception):
    """Error in application configuration."""
    pass

class ValidationError(Exception):
    """Error in request validation."""
    pass

def validate_environment() -> None:
    """Validate required environment variables."""
    required_vars = ['FRED_API_KEY', 'ANTHROPIC_API_KEY', 'CLAUDE_MODEL']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        raise ConfigurationError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Load and validate environment variables
logger.info("Loading environment variables...")
load_dotenv(override=True)
try:
    validate_environment()
    logger.info("Environment variables loaded and validated:")
    logger.info(f"FRED_API_KEY: {'set' if os.environ.get('FRED_API_KEY') else 'not set'}")
    logger.info(f"ANTHROPIC_API_KEY: {'set' if os.environ.get('ANTHROPIC_API_KEY') else 'not set'}")
    logger.info(f"CLAUDE_MODEL: {os.environ.get('CLAUDE_MODEL')}")
except ConfigurationError as e:
    logger.error(f"Environment validation failed: {str(e)}")
    raise

# Import InflationTracker after environment variables are loaded
from services.inflation_tracker import (
    InflationTracker, 
    TrackerError, 
    ServiceInitializationError,
    DataProcessingError,
    BackupError
)

app = Flask(__name__)
CORS(app)

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["1 per second"],  # Strict default limit for testing
    storage_uri="memory://"  # Use in-memory storage for testing
)

# Security headers middleware
@app.after_request
def add_security_headers(response: Response) -> Response:
    """Add security headers to response."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# Request logging middleware
@app.before_request
def log_request_info() -> None:
    """Log request details."""
    logger.info(f"Request: {request.method} {request.url}")
    logger.debug(f"Headers: {dict(request.headers)}")
    logger.debug(f"Body: {request.get_data()}")

def handle_errors(f):
    """Decorator for consistent error handling."""
    @wraps(f)
    def wrapper(*args, **kwargs) -> Tuple[Dict[str, Any], int]:
        try:
            return f(*args, **kwargs)
        except ServiceInitializationError as e:
            logger.error(f"Service initialization error: {str(e)}")
            return jsonify({
                'status': 'Error',
                'error': 'Service unavailable',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }), 503
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return jsonify({
                'status': 'Error',
                'error': 'Invalid request',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }), 400
        except DataProcessingError as e:
            logger.error(f"Data processing error: {str(e)}")
            return jsonify({
                'status': 'Error',
                'error': 'Processing failed',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }), 422
        except BackupError as e:
            logger.error(f"Backup error: {str(e)}")
            return jsonify({
                'status': 'Error',
                'error': 'Backup failed',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({
                'status': 'Error',
                'error': 'Internal server error',
                'message': 'An unexpected error occurred',
                'timestamp': datetime.now().isoformat()
            }), 500
    return wrapper

# Initialize FRED API client
try:
    fred_client = InflationTracker()
except Exception as e:
    logger.error(f"Failed to initialize FRED client: {str(e)}")
    fred_client = None

def validate_client() -> None:
    """Validate FRED client is initialized."""
    if not fred_client:
        raise ServiceInitializationError('FRED client not initialized')

@app.route('/api/v1/health', methods=['GET'])
@limiter.exempt
def health_check() -> Tuple[Dict[str, Any], int]:
    """Health check endpoint."""
    try:
        validate_client()
        status = fred_client.get_status()
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'services': status
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 503

@app.route('/api/v1/inflation/initialize', methods=['POST'])
@limiter.limit("1 per second")  # Strict limit for testing
@handle_errors
def initialize_data() -> Tuple[Dict[str, Any], int]:
    """Initialize the database with historical data."""
    validate_client()
    result = fred_client.fetch_and_store_historical_data()
    return jsonify(result), 200

@app.route('/api/v1/inflation/update', methods=['POST'])
@limiter.limit("1 per second")  # Strict limit for testing
@handle_errors
def update_data() -> Tuple[Dict[str, Any], int]:
    """Update data with latest values."""
    validate_client()
    result = fred_client.update_daily_data()
    return jsonify(result), 200

@app.route('/api/v1/inflation/backup', methods=['POST'])
@limiter.limit("1 per second")  # Strict limit for testing
@handle_errors
def backup_data() -> Tuple[Dict[str, Any], int]:
    """Create a backup of the database."""
    validate_client()
    result = fred_client.backup_data()
    return jsonify(result), 200

@app.route('/api/v1/inflation/data', methods=['GET'])
@limiter.limit("1 per second")  # Strict limit for testing
@handle_errors
def get_inflation_data() -> Tuple[Dict[str, Any], int]:
    """Get current inflation data."""
    validate_client()
    data = fred_client.get_inflation_data()
    
    # Validate response data
    if not isinstance(data, dict):
        raise ValidationError("Invalid response format")
    if 'status' not in data:
        raise ValidationError("Missing status in response")
    
    return jsonify(data), 200

@app.errorhandler(429)
def ratelimit_handler(e) -> Tuple[Dict[str, Any], int]:
    """Handle rate limit exceeded."""
    return jsonify({
        'status': 'Error',
        'error': 'Rate limit exceeded',
        'message': str(e.description),
        'timestamp': datetime.now().isoformat()
    }), 429

if __name__ == '__main__':
    # Validate environment before starting
    try:
        validate_environment()
        # Run the Flask app in debug mode on port 5003
        app.run(host='0.0.0.0', port=5003, debug=True)
    except ConfigurationError as e:
        logger.error(f"Failed to start application: {str(e)}")
        exit(1)
