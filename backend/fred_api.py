"""
FRED API integration module.

This module provides functions for interacting with the Federal Reserve Economic Data (FRED) API.
"""

import os
from fredapi import Fred
from typing import Optional

def get_fred_client(api_key: Optional[str] = None) -> Fred:
    """
    Get a FRED API client instance.
    
    Args:
        api_key (Optional[str]): FRED API key. If not provided, will try to get from environment.
    
    Returns:
        Fred: FRED API client instance
    
    Raises:
        ValueError: If no API key is provided and none found in environment
    """
    api_key = api_key or os.getenv('FRED_API_KEY')
    if not api_key:
        raise ValueError("FRED API key not found. Set FRED_API_KEY environment variable.")
    return Fred(api_key=api_key)

__all__ = ['get_fred_client']
