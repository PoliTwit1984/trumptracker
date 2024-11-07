import anthropic
import logging
from typing import Dict, Any
import time
from datetime import datetime, timedelta
from functools import wraps
from ..database import get_session, store_series_analysis

logger = logging.getLogger(__name__)

class AnalyzerError(Exception):
    """Base exception for analyzer errors."""
    pass

class AnalysisCache:
    def __init__(self, ttl_seconds: int = 300):  # 5 minutes TTL
        self.cache = {}
        self.ttl = ttl_seconds
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum 1 second between requests

    def get(self, key: str) -> Any:
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() - entry['timestamp'] < timedelta(seconds=self.ttl):
                return entry['data']
            else:
                del self.cache[key]
        return None

    def set(self, key: str, data: Any) -> None:
        self.cache[key] = {
            'data': data,
            'timestamp': datetime.now()
        }

    def wait_if_needed(self) -> None:
        """Implement rate limiting."""
        now = time.time()
        time_since_last_request = now - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)
        self.last_request_time = time.time()

class InflationAnalyzer:
    def __init__(self):
        """Initialize Anthropic client and cache."""
        try:
            self.anthropic_client = anthropic.Anthropic()
            self.cache = AnalysisCache()
            self.model = self._validate_model()
            logger.info(f"Using Claude model: {self.model}")
        except Exception as e:
            raise AnalyzerError(f"Failed to initialize analyzer: {str(e)}")

    def _validate_model(self) -> str:
        """Get and validate Claude model name."""
        return 'claude-3-5-sonnet-20241022'

    def _generate_cache_key(self, metrics: Dict) -> str:
        """Generate a cache key based on metrics data."""
        key_parts = []
        for name, data in sorted(metrics.items()):
            if 'current_value' in data and 'percentage_change' in data:
                key_parts.append(f"{name}:{data['current_value']}:{data['percentage_change']}")
        return "|".join(key_parts)

    def _get_metric_prompt(self, metric_name: str, data: Dict) -> str:
        """Get the appropriate analysis prompt for each metric type."""
        date_context = """The current date is 11/6/2024 regardless of what you think and you will analyze data before this date since the data reporting lags a month or two behind the current date. You should analyze the available historical data and provide insights based on the trends and patterns shown in that data."""

        if metric_name == 'cpi':
            return f"""{date_context}

Using the available CPI-U data (current value: {data['current_value']} {data['units']}), analyze:
1. Year-over-year percentage change
2. 3-month trend analysis
3. Key drivers of changes
4. Comparison to Federal Reserve's 2% target
5. Impact on consumer purchasing power
6. Seasonal adjustment factors
7. Notable category changes

Format the analysis with:
- Key statistics at the top
- Trend visualization suggestions
- Forward-looking indicators
- Consumer impact assessment

Note: Base your analysis on the historical data available through {data['last_updated']}, which shows a current value of {data['current_value']} and a year-over-year change of {data['percentage_change']}%."""
        elif metric_name == 'core_cpi':
            return f"""{date_context}

Using the available Core CPI data (current value: {data['current_value']} {data['units']}), examine:
1. Underlying inflation trends excluding volatile components
2. Month-over-month changes in:
   - Housing costs
   - Medical care
   - Education
   - Transportation
3. Sticky price components
4. Service sector inflation
5. Goods inflation
6. Wage pressure indicators

Present findings as:
- Primary pressure points
- Structural vs cyclical factors
- Policy implications

Note: Base your analysis on the historical data available through {data['last_updated']}, which shows a current value of {data['current_value']} and a year-over-year change of {data['percentage_change']}%."""
        elif metric_name == 'food':
            return f"""{date_context}

Using the available Food CPI data (current value: {data['current_value']} {data['units']}), analyze:
1. Categories showing largest increases/decreases:
   - Grocery store items
   - Restaurant prices
   - Fresh vs processed foods
2. Supply chain impacts
3. Agricultural commodity price effects
4. Regional variations
5. Seasonal factors

Include:
- Category-specific trends
- Consumer substitution patterns
- Price elasticity impacts

Note: Base your analysis on the historical data available through {data['last_updated']}, which shows a current value of {data['current_value']} and a year-over-year change of {data['percentage_change']}%."""
        elif metric_name == 'gas':
            return f"""{date_context}

Using the available gas price data (current value: {data['current_value']} {data['units']}), analyze:
1. National average vs regional breakdowns
2. Price changes by grade:
   - Regular
   - Mid-grade
   - Premium
   - Diesel
3. Compare to:
   - Previous week
   - Month ago
   - Year ago
4. Impact factors:
   - Crude oil prices
   - Refinery capacity
   - Seasonal demand
   - Global events

Output format:
- Price trends by region
- Supply/demand dynamics
- Short-term forecast

Note: Base your analysis on the historical data available through {data['last_updated']}, which shows a current value of {data['current_value']} and a year-over-year change of {data['percentage_change']}%."""
        else:  # housing
            return f"""{date_context}

Using the available Case-Shiller Housing Price Index data (current value: {data['current_value']} {data['units']}), analyze:
1. National price trends
2. Top 20 metropolitan areas:
   - Highest/lowest appreciation
   - Market velocity
   - Price tier performance
3. Compare with:
   - Mortgage rates
   - Housing inventory
   - Days on market
   - New construction
4. Affordability metrics

Provide:
- Market heat map suggestions
- Regional comparisons
- Leading indicator analysis
- Affordability index trends

Note: Base your analysis on the historical data available through {data['last_updated']}, which shows a current value of {data['current_value']} and a year-over-year change of {data['percentage_change']}%."""

    def analyze_trends(self, metrics: Dict) -> str:
        """Analyze inflation trends with caching and rate limiting."""
        try:
            # Generate cache key from metrics
            cache_key = self._generate_cache_key(metrics)
            
            # Check cache first
            cached_analysis = self.cache.get(cache_key)
            if cached_analysis:
                logger.info("Using cached analysis")
                return cached_analysis

            # Implement rate limiting
            self.cache.wait_if_needed()

            session = get_session()
            try:
                # Analyze each metric individually with specific prompts
                for metric_name, data in metrics.items():
                    prompt = self._get_metric_prompt(metric_name, data)
                    
                    logger.info(f"Sending analysis request to Claude for {metric_name}")
                    try:
                        response = self.anthropic_client.messages.create(
                            model=self.model,
                            max_tokens=1024,
                            messages=[
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ],
                            temperature=0,
                            system="You are an expert economic analyst providing insights on inflation metrics."
                        )
                        
                        analysis = response.content[0].text if isinstance(response.content, list) else response.content
                        
                        # Store analysis in database
                        series_id = metrics[metric_name].get('series_id')
                        if series_id:
                            store_series_analysis(session, series_id, analysis)
                            
                    except anthropic.RateLimitError:
                        logger.warning(f"Rate limit hit for {metric_name}")
                        continue
                    except anthropic.APIError as e:
                        logger.error(f"Claude API error for {metric_name}: {str(e)}")
                        continue

                # Return combined analysis
                return "Analysis updated in database"

            finally:
                session.close()

        except Exception as e:
            logger.error(f"Error analyzing trends: {str(e)}")
            return "Unable to generate analysis at this time."
