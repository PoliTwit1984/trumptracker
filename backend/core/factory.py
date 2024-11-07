from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from backend.core.config import AppConfig
from backend.core.exceptions import handle_rate_limit_exceeded
from backend.middleware.security import add_security_headers, log_request_info
from backend.api.routes import api

def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configure CORS
    if AppConfig.CORS_ENABLED:
        CORS(app)
    
    # Configure rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["5 per second"],  # More lenient default limit
        storage_uri=AppConfig.RATE_LIMIT_STORAGE
    )
    
    # Register error handlers
    app.errorhandler(429)(handle_rate_limit_exceeded)
    
    # Register middleware
    app.after_request(add_security_headers)
    app.before_request(log_request_info)
    
    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')
    
    return app
