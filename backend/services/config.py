import os

def get_fred_api_key() -> str:
    """Get FRED API key from environment variables."""
    api_key = os.getenv('FRED_API_KEY', '')
    if not api_key:
        raise ValueError("FRED_API_KEY environment variable is not set")
    return api_key

def get_claude_model() -> str:
    """Get Claude model name from environment variables."""
    return os.getenv('CLAUDE_MODEL', 'claude-3-5-sonnet-20241022')

# FRED API Series IDs
SERIES_IDS = {
    'cpi': 'CPIAUCSL',           # Consumer Price Index for All Urban Consumers
    'core_cpi': 'CPILFESL',      # Core Consumer Price Index (excluding food and energy)
    'food': 'CPIUFDSL',          # Consumer Price Index: Food
    'gas': 'GASREGW',            # US Regular All Formulations Gas Price
    'housing': 'CSUSHPISA'       # Case-Shiller Home Price Index
}

# Historical data start dates - Updated to get more recent data
HISTORICAL_START_DATES = {
    'CPIAUCSL': '2024-01-01',    # Monthly, released on 13th
    'CPILFESL': '2024-01-01',    # Monthly, released on 13th
    'CPIUFDSL': '2024-01-01',    # Monthly, released on 13th
    'GASREGW': '2024-01-01',     # Weekly, released on Tuesday
    'CSUSHPISA': '2024-01-01'    # Monthly, released on last Tuesday
}
