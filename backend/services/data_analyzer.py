import anthropic
import logging
from typing import Dict, Any
import time
from datetime import datetime, timedelta
from functools import wraps

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

            # Prepare the analysis prompt
            prompt = self._prepare_analysis_prompt(metrics)
            
            logger.info("Sending analysis request to Claude")
            try:
                # Create a message using the latest model version
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
                
                logger.info("Received response from Claude")
                
                # Extract the analysis text
                analysis = response.content[0].text if isinstance(response.content, list) else response.content
                
                # Cache the result
                self.cache.set(cache_key, analysis)
                
                return analysis
                
            except anthropic.RateLimitError:
                logger.warning("Rate limit hit, using cached analysis if available")
                return cached_analysis or "Analysis temporarily unavailable due to rate limiting."
                
            except anthropic.APIError as e:
                logger.error(f"Claude API error: {str(e)}")
                return cached_analysis or "Analysis temporarily unavailable."

        except Exception as e:
            logger.error(f"Error analyzing trends: {str(e)}")
            return "Unable to generate analysis at this time."

    def _prepare_analysis_prompt(self, metrics: Dict) -> str:
        """Prepare the analysis prompt from metrics data."""
        try:
            data_summary = []
            for name, data in metrics.items():
                if 'percentage_change' in data and 'historical_data' in data:
                    summary = (
                        f"{data['title']}: {data['percentage_change']:.2f}% change over past year\n"
                        f"Current value: {data['current_value']:.2f} {data['units']}\n"
                        f"Year ago value: {data['baseline_value']:.2f} {data['units']}"
                    )
                    data_summary.append(summary)

            if not data_summary:
                raise ValueError("No valid data available for prompt generation")

            prompt = f"""As of November 5th, 2024 (day after Trump's election), analyze these inflation metrics:

{'\n\n'.join(data_summary)}

Please provide a concise analysis focusing on:
1. The current state of inflation metrics
2. Key areas showing significant changes over the past year
3. Potential economic implications going forward

Keep in mind this analysis is being done on the day after the 2024 presidential election.
"""
            return prompt

        except Exception as e:
            logger.error(f"Error preparing analysis prompt: {str(e)}")
            raise
