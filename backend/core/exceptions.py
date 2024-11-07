from datetime import datetime
from typing import Dict, Any, Tuple
from flask import jsonify
import logging
import traceback
from functools import wraps

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Error in request validation."""
    pass

class ServiceInitializationError(Exception):
    """Error in service initialization."""
    pass

class DataProcessingError(Exception):
    """Error in data processing."""
    pass

class BackupError(Exception):
    """Error in backup operation."""
    pass

def create_error_response(error: str, message: str, status: str = 'Error') -> Dict[str, Any]:
    """Create a standardized error response."""
    return {
        'status': status,
        'error': error,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }

def handle_errors(f):
    """Decorator for consistent error handling across routes."""
    @wraps(f)
    def wrapper(*args, **kwargs) -> Tuple[Dict[str, Any], int]:
        try:
            return f(*args, **kwargs)
        except ServiceInitializationError as e:
            logger.error(f"Service initialization error: {str(e)}")
            return jsonify(create_error_response(
                'Service unavailable',
                str(e)
            )), 503
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return jsonify(create_error_response(
                'Invalid request',
                str(e)
            )), 400
        except DataProcessingError as e:
            logger.error(f"Data processing error: {str(e)}")
            return jsonify(create_error_response(
                'Processing failed',
                str(e)
            )), 422
        except BackupError as e:
            logger.error(f"Backup error: {str(e)}")
            return jsonify(create_error_response(
                'Backup failed',
                str(e)
            )), 500
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify(create_error_response(
                'Internal server error',
                'An unexpected error occurred'
            )), 500
    return wrapper

def handle_rate_limit_exceeded(e) -> Tuple[Dict[str, Any], int]:
    """Handle rate limit exceeded errors."""
    return jsonify(create_error_response(
        'Rate limit exceeded',
        str(e.description)
    )), 429
