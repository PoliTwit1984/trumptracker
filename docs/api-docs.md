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
