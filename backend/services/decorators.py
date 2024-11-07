"""Decorators for the inflation tracking service."""

import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)

def retry_on_failure(max_retries: int = 3, delay: int = 1):
    """Decorator to retry operations on failure with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            last_error = None
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    last_error = e
                    if retries == max_retries:
                        logger.error(f"Max retries ({max_retries}) reached for {func.__name__}")
                        raise
                    wait_time = delay * (2 ** (retries - 1))
                    logger.warning(f"Attempt {retries} failed for {func.__name__}. "
                                 f"Retrying in {wait_time}s. Error: {str(e)}")
                    time.sleep(wait_time)
            if last_error:
                raise last_error
            return None
        return wrapper
    return decorator
