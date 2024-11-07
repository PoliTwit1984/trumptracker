"""
Trump Tracker Backend Package

This package provides functionality for tracking and analyzing economic promises
through FRED data integration and AI-powered analysis.
"""

from backend.services.inflation_tracker import InflationTracker
from backend.services.data_fetcher import FREDDataFetcher
from backend.services.data_analyzer import InflationAnalyzer
from backend.services.config import SERIES_IDS, HISTORICAL_START_DATES
from backend.database import get_session
from backend.fred_api import get_fred_client

__all__ = [
    'InflationTracker',
    'FREDDataFetcher',
    'InflationAnalyzer',
    'SERIES_IDS',
    'HISTORICAL_START_DATES',
    'get_session',
    'get_fred_client'
]

__version__ = '1.0.0'
