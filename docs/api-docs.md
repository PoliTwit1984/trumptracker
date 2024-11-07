# API Documentation

## Base URL
`http://localhost:5003/api/v1`

## Endpoints

### Get Inflation Data
```
GET /inflation/data
```

Returns current inflation metrics and analysis.

#### Response
```json
{
  "status": "Success",
  "metrics": {
    "cpi": {
      "title": "Consumer Price Index for All Urban Consumers: All Items in U.S. City Average",
      "current_value": 314.686,
      "baseline_value": 308.742,
      "percentage_change": 1.93,
      "historical_data": [
        {
          "date": "2023-11-01",
          "value": 308.742
        },
        // ... more data points
      ],
      "units": "Index 1982-1984=100",
      "last_updated": "2024-11-06"
    },
    "core_cpi": {
      // Similar structure to cpi
    },
    "food": {
      // Similar structure to cpi
    },
    "gas": {
      // Similar structure to cpi
    },
    "housing": {
      // Similar structure to cpi
    }
  },
  "analysis": "AI-generated analysis of trends",
  "timestamp": "2024-11-06T20:28:53.782219"
}
```

### Initialize Historical Data
```
POST /inflation/initialize
```

Fetches and stores historical data for all metrics.

#### Response
```json
{
  "status": "Success",
  "message": "Historical data fetched and stored successfully",
  "timestamp": "2024-11-06T20:12:48.488283"
}
```

### Update Data
```
POST /inflation/update
```

Updates data with latest values from FRED API.

#### Response
```json
{
  "status": "Success",
  "message": "Data updated successfully",
  "timestamp": "2024-11-06T20:12:48.488283"
}
```

### Backup Database
```
POST /inflation/backup
```

Creates a backup of the current database.

#### Response
```json
{
  "status": "Success",
  "message": "Database backup created successfully",
  "timestamp": "2024-11-06T20:12:48.488283"
}
```

### Health Check
```
GET /health
```

Returns service health status.

#### Response
```json
{
  "status": "healthy",
  "timestamp": "2024-11-06T20:12:48.488283",
  "version": "1.0.0",
  "services": {
    "data_fetcher": "healthy",
    "analyzer": "healthy"
  }
}
```

## Error Responses

All endpoints may return the following error responses:

### Rate Limit Exceeded
```json
{
  "error": "Rate limit exceeded",
  "status": "error",
  "timestamp": "2024-11-06T20:12:48.488283"
}
```

### Service Error
```json
{
  "error": "Internal server error",
  "status": "error",
  "timestamp": "2024-11-06T20:12:48.488283"
}
```

### Validation Error
```json
{
  "error": "Invalid request parameters",
  "status": "error",
  "timestamp": "2024-11-06T20:12:48.488283"
}
```

## To Do
1. Add authentication endpoints
2. Add data export endpoints
3. Add admin endpoints
4. Add metric configuration endpoints
5. Add data comparison endpoints
6. Add data versioning endpoints
7. Add monitoring endpoints
8. Add rate limit configuration endpoints
9. Add webhook configuration endpoints
10. Add data validation endpoints
