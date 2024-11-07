import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_fred_api_key() -> str:
    """Get FRED API key from environment variables."""
    return os.getenv('FRED_API_KEY', '')

def get_claude_model() -> str:
    """Get Claude model name from environment variables."""
    return os.getenv('CLAUDE_MODEL', 'claude-3-opus-20240229')

# FRED API Series IDs
SERIES_IDS = {
    'cpi': 'CPIAUCSL',           # Consumer Price Index for All Urban Consumers
    'core_cpi': 'CPILFESL',      # Core Consumer Price Index (excluding food and energy)
    'food': 'CPIUFDSL',          # Consumer Price Index: Food
    'gas': 'GASREGW',            # US Regular All Formulations Gas Price
    'housing': 'CSUSHPISA'       # Case-Shiller Home Price Index
}

# Historical data start dates
HISTORICAL_START_DATES = {
    'CPIAUCSL': '2020-01-01',
    'CPILFESL': '2020-01-01',
    'CPIUFDSL': '2020-01-01',
    'GASREGW': '2020-01-01',
    'CSUSHPISA': '2020-01-01'
}
