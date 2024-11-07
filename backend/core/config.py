import os
from dotenv import load_dotenv
import logging
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ConfigurationError(Exception):
    """Error in application configuration."""
    pass

def validate_environment() -> None:
    """Validate required environment variables."""
    required_vars = ['FRED_API_KEY', 'ANTHROPIC_API_KEY']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        raise ConfigurationError(f"Missing required environment variables: {', '.join(missing_vars)}")

def init_environment() -> None:
    """Initialize and validate environment variables."""
    logger.info("Loading environment variables...")
    load_dotenv(override=True)
    try:
        validate_environment()
        logger.info("Environment variables loaded and validated:")
        logger.info(f"FRED_API_KEY: {'set' if os.environ.get('FRED_API_KEY') else 'not set'}")
        logger.info(f"ANTHROPIC_API_KEY: {'set' if os.environ.get('ANTHROPIC_API_KEY') else 'not set'}")
        logger.info(f"CLAUDE_MODEL: {os.environ.get('CLAUDE_MODEL', 'claude-3-sonnet-20240229')}")
        # Set default model if not provided
        if not os.environ.get('CLAUDE_MODEL'):
            os.environ['CLAUDE_MODEL'] = 'claude-3-sonnet-20240229'
    except ConfigurationError as e:
        logger.error(f"Environment validation failed: {str(e)}")
        raise

class AppConfig:
    """Application configuration settings."""
    DEBUG: bool = True
    HOST: str = '0.0.0.0'
    PORT: int = 5003
    RATE_LIMIT_DEFAULT: str = "1 per second"
    RATE_LIMIT_STORAGE: str = "memory://"
    CORS_ENABLED: bool = True
    
    # Security Headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
    }
