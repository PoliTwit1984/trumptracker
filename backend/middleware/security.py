from flask import Response, request
import logging
from backend.core.config import AppConfig

logger = logging.getLogger(__name__)

def add_security_headers(response: Response) -> Response:
    """Add security headers to response."""
    for header, value in AppConfig.SECURITY_HEADERS.items():
        response.headers[header] = value
    return response

def log_request_info() -> None:
    """Log request details."""
    logger.info(f"Request: {request.method} {request.url}")
    logger.debug(f"Headers: {dict(request.headers)}")
    logger.debug(f"Body: {request.get_data()}")
