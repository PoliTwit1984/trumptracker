# API Documentation

## Endpoints

### GET /api/promises
Returns a list of all tracked promises, grouped by category.

#### Response Format
```json
{
  "Inflation": [
    {
      "id": 1,
      "title": "Lower Consumer Prices",
      "category": "Inflation",
      "status": "In Progress",
      "description": "Promise to reduce the Consumer Price Index (CPI)",
      "metric_type": "cpi",
      "last_updated": "2024-11-05"
    }
  ]
}
```

### GET /api/inflation-data
Returns current inflation metrics with historical data.

#### Response Format
```json
{
  "status": "Success",
  "last_updated": "2024-11-05",
  "metrics": {
    "cpi": {
      "current_value": 314.69,
      "baseline_value": 308.02,
      "percentage_change": 2.16,
      "historical_data": [...],
      "title": "Consumer Price Index",
      "units": "Index 1982-1984=100"
    }
  },
  "analysis": "AI-generated analysis of trends"
}
```

## Error Handling

All endpoints use standard HTTP status codes and return detailed error messages:

### Error Response Format
```json
{
  "status": "Error",
  "error": "Detailed error message",
  "code": "ERROR_CODE"
}
```

### Common Error Codes
- `VALIDATION_ERROR`: Invalid input data
- `SERVICE_ERROR`: Service initialization or processing error
- `API_ERROR`: External API error (FRED or Claude)
- `DATA_ERROR`: Data processing or validation error
- `BACKUP_ERROR`: Database backup error

### HTTP Status Codes
- 200: Success
- 400: Bad Request (validation errors)
- 401: Unauthorized (invalid API key)
- 404: Not Found
- 429: Too Many Requests (rate limit)
- 500: Internal Server Error
- 503: Service Unavailable

## Data Validation

All endpoints perform strict data validation:

### Input Validation
- API keys must be valid
- Date formats must be ISO 8601
- Numeric values must be valid floats
- Required fields must be present

### Output Validation
- Response format is validated
- Data types are checked
- Required fields are verified
- Metrics data is validated

## Service Architecture

The API is built on a modular service architecture:

### Core Services
- `data_fetcher.py`: FRED data operations
- `data_analyzer.py`: AI analysis
- `inflation_tracker.py`: Service coordination

### Support Modules
- `validators.py`: Data validation
- `exceptions.py`: Error handling
- `decorators.py`: Utility functions

## Rate Limiting

To ensure service stability:
- 100 requests per minute per IP
- 1000 requests per hour per IP
- Retry-After header included in 429 responses

## Testing

API endpoints can be tested using:
```bash
# Run all API tests
python -m pytest tests/test_app.py

# Run specific endpoint tests
python -m pytest tests/test_app.py::test_get_promises
python -m pytest tests/test_app.py::test_get_inflation_data
```

## Future Enhancements
- Authentication
- Request batching
- Response compression
- Caching layer
- Metrics collection
- Performance monitoring
