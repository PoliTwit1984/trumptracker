import logging
from backend.core.config import init_environment
from backend.core.factory import create_app
from backend.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main application entry point."""
    try:
        # Initialize environment variables
        init_environment()
        
        # Initialize database
        init_db()
        
        # Create and run Flask application
        app = create_app()
        app.run(host='0.0.0.0', port=5003, debug=True)
        
    except Exception as e:
        logger.error(f"Application startup failed: {str(e)}")
        raise

if __name__ == '__main__':
    main()
