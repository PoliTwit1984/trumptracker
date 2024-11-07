import anthropic
import logging
from typing import Dict, List, Optional, Any
import time
from datetime import datetime
from functools import wraps
import json
import re
from .config import get_claude_model

logger = logging.getLogger(__name__)

class AnalyzerError(Exception):
    """Base exception for analyzer errors."""
    pass

class ValidationError(AnalyzerError):
    """Validation error for input data."""
    pass

class APIError(AnalyzerError):
    """Error during API communication."""
    pass

class PromptError(AnalyzerError):
    """Error in prompt generation."""
    pass

def retry_on_failure(max_retries: int = 3, delay: int = 1):
    """Decorator to retry operations on failure with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (anthropic.APIError, anthropic.RateLimitError) as e:
                    retries += 1
                    if retries == max_retries:
                        logger.error(f"Max retries ({max_retries}) reached for {func.__name__}")
                        raise APIError(f"Failed after {max_retries} retries: {str(e)}")
                    wait_time = delay * (2 ** (retries - 1))
                    logger.warning(f"Attempt {retries} failed for {func.__name__}. Retrying in {wait_time}s. Error: {str(e)}")
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator

class InflationAnalyzer:
    def __init__(self):
        """Initialize Anthropic client and get Claude model with validation."""
        try:
            self.anthropic_client = anthropic.Anthropic()
            self.claude_model = self._validate_model(get_claude_model())
            logger.info(f"Using Claude model: {self.claude_model}")
        except Exception as e:
            raise AnalyzerError(f"Failed to initialize analyzer: {str(e)}")

    def _validate_model(self, model: str) -> str:
        """Validate Claude model name."""
        valid_models = ['claude-3-opus-20240229', 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307']
        if not model or not isinstance(model, str):
            raise ValidationError("Model name must be a non-empty string")
        if model not in valid_models:
            raise ValidationError(f"Invalid model name. Must be one of: {', '.join(valid_models)}")
        return model

    def _validate_metrics(self, metrics: Dict) -> None:
        """Validate metrics data structure."""
        if not isinstance(metrics, dict):
            raise ValidationError("Metrics must be a dictionary")
        
        required_fields = ['title', 'percentage_change', 'current_value', 'baseline_value', 'units', 'historical_data']
        
        for name, data in metrics.items():
            if not isinstance(name, str):
                raise ValidationError(f"Metric name must be a string, got {type(name)}")
            
            if not isinstance(data, dict):
                raise ValidationError(f"Metric data must be a dictionary for {name}")
            
            # Check required fields
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                raise ValidationError(f"Missing required fields for {name}: {', '.join(missing_fields)}")
            
            # Validate numeric fields
            for field in ['percentage_change', 'current_value', 'baseline_value']:
                if not isinstance(data[field], (int, float)):
                    raise ValidationError(f"Field {field} must be numeric for {name}")
            
            # Validate historical data
            if not isinstance(data['historical_data'], list):
                raise ValidationError(f"Historical data must be a list for {name}")
            
            for point in data['historical_data']:
                if not isinstance(point, dict) or 'date' not in point or 'value' not in point:
                    raise ValidationError(f"Invalid historical data point format for {name}")
                try:
                    datetime.strptime(point['date'], '%Y-%m-%d')
                except ValueError:
                    raise ValidationError(f"Invalid date format in historical data for {name}")

    def _validate_prompt(self, prompt: str) -> None:
        """Validate analysis prompt."""
        if not isinstance(prompt, str):
            raise PromptError("Prompt must be a string")
        if not prompt.strip():
            raise PromptError("Prompt cannot be empty")
        if len(prompt) > 4000:  # Arbitrary limit to prevent excessive tokens
            raise PromptError("Prompt exceeds maximum length")

    def _validate_analysis_output(self, analysis: str) -> bool:
        """Validate analysis output meets quality standards."""
        if not isinstance(analysis, str) or not analysis.strip():
            return False
        
        # Check minimum length (arbitrary threshold)
        if len(analysis) < 100:
            return False
        
        # Check for required analysis components
        required_components = [
            r'current state',
            r'change|trend',
            r'implication|impact|effect'
        ]
        
        for component in required_components:
            if not re.search(component, analysis, re.IGNORECASE):
                return False
        
        return True

    def _prepare_analysis_prompt(self, metrics: Dict) -> str:
        """Prepare the analysis prompt from metrics data with validation."""
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
                raise PromptError("No valid data available for prompt generation")

            prompt = f"""As of November 5th, 2024 (day after Trump's election), analyze these inflation metrics:

{'\n\n'.join(data_summary)}

Please provide a concise analysis focusing on:
1. The current state of inflation metrics
2. Key areas showing significant changes over the past year
3. Potential economic implications going forward

Keep in mind this analysis is being done on the day after the 2024 presidential election.
"""
            self._validate_prompt(prompt)
            return prompt

        except Exception as e:
            raise PromptError(f"Failed to prepare analysis prompt: {str(e)}")

    @retry_on_failure(max_retries=3, delay=1)
    def analyze_trends(self, metrics: Dict) -> str:
        """Use Claude to analyze inflation trends with comprehensive validation and error handling."""
        try:
            # Validate input metrics
            self._validate_metrics(metrics)
            
            # Prepare and validate prompt
            prompt = self._prepare_analysis_prompt(metrics)
            
            logger.info("Sending analysis request to Claude")
            logger.debug(f"Prompt: {prompt}")
            
            try:
                # Create a message using the latest model version
                response = self.anthropic_client.messages.create(
                    model=self.claude_model,
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
                
                analysis = str(response.content)
                
                # Validate analysis output
                if not self._validate_analysis_output(analysis):
                    logger.warning("Analysis output failed quality validation")
                    return "Unable to generate quality analysis at this time."
                
                return analysis
                
            except anthropic.RateLimitError as e:
                logger.error(f"Rate limit exceeded: {str(e)}")
                raise APIError("Rate limit exceeded, please try again later")
                
            except anthropic.APIError as e:
                logger.error(f"Claude API error: {str(e)}")
                if hasattr(e, 'status_code'):
                    logger.error(f"Status code: {e.status_code}")
                if hasattr(e, 'response'):
                    logger.error(f"Response: {e.response}")
                raise APIError(f"API error: {str(e)}")

        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return f"Error in input data: {str(e)}"
            
        except PromptError as e:
            logger.error(f"Prompt error: {str(e)}")
            return "Unable to generate analysis prompt"
            
        except Exception as e:
            logger.error(f"Unexpected error analyzing trends: {str(e)}")
            return "An unexpected error occurred during analysis"
