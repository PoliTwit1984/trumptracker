from flask import jsonify, Blueprint
from datetime import datetime
from typing import Dict, Any, Tuple
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from backend.core.exceptions import handle_errors, ServiceInitializationError, ValidationError
from backend.services.inflation_tracker import InflationTracker
import logging

logger = logging.getLogger(__name__)

# Create Blueprint for API routes
api = Blueprint('api', __name__)

# Initialize FRED API client as a global variable
fred_client = None

def get_fred_client():
    """Get or initialize FRED client."""
    global fred_client
    if fred_client is None:
        try:
            fred_client = InflationTracker()
            logger.info("FRED client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize FRED client: {str(e)}")
            raise ServiceInitializationError(f"Failed to initialize FRED client: {str(e)}")
    return fred_client

def validate_client() -> None:
    """Validate FRED client is initialized."""
    if get_fred_client() is None:
        raise ServiceInitializationError('FRED client not initialized')

@api.route('/v1/health', methods=['GET'])
def health_check() -> Tuple[Dict[str, Any], int]:
    """Health check endpoint."""
    try:
        client = get_fred_client()
        status = client.get_status()
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'services': status
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 503

@api.route('/v1/inflation/initialize', methods=['POST'])
@handle_errors
def initialize_data() -> Tuple[Dict[str, Any], int]:
    """Initialize the database with historical data."""
    client = get_fred_client()
    result = client.fetch_and_store_historical_data()
    return jsonify(result), 200

@api.route('/v1/inflation/update', methods=['POST'])
@handle_errors
def update_data() -> Tuple[Dict[str, Any], int]:
    """Update data with latest values."""
    client = get_fred_client()
    result = client.update_daily_data()
    return jsonify(result), 200

@api.route('/v1/inflation/backup', methods=['POST'])
@handle_errors
def backup_data() -> Tuple[Dict[str, Any], int]:
    """Create a backup of the database."""
    client = get_fred_client()
    result = client.backup_data()
    return jsonify(result), 200

@api.route('/v1/inflation/data', methods=['GET'])
@handle_errors
def get_inflation_data() -> Tuple[Dict[str, Any], int]:
    """Get current inflation data."""
    client = get_fred_client()
    data = client.get_inflation_data()
    
    # Log response data for debugging
    logger.info("API Response Data:")
    logger.info(f"Metrics: {list(data.get('metrics', {}).keys())}")
    logger.info(f"Analysis present: {'analysis' in data}")
    logger.info(f"Timestamp: {data.get('timestamp')}")
    
    return jsonify(data), 200
