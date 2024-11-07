# API Documentation

## Base URL
`http://localhost:5003/api/v1`

## Current Endpoints

### Inflation Data

#### GET /inflation/data
Retrieves current inflation metrics and analysis.

**Response**
```json
{
  "status": "Success",
  "metrics": {
    "cpi": {
      "current_value": number,
      "baseline_value": number,
      "percentage_change": number,
      "historical_data": array,
      "units": string,
      "last_updated": string,
      "analysis": string
    },
    "core_cpi": {...},
    "food": {...},
    "gas": {...},
    "housing": {...}
  },
  "timestamp": string
}
```

#### POST /inflation/update
Triggers a data update and analysis refresh.

**Response**
```json
{
  "status": "Success",
  "message": "Data updated successfully",
  "timestamp": string
}
```

## Planned Endpoints

### Campaign Promises

#### GET /promises
Retrieves all campaign promises.

**Response**
```json
{
  "status": "Success",
  "promises": [
    {
      "id": string,
      "category": string,
      "text": string,
      "source": string,
      "source_link": string,
      "status": "waiting" | "completed",
      "completion_date": string | null,
      "created_at": string,
      "updated_at": string
    }
  ],
  "timestamp": string
}
```

#### GET /promises/{category}
Retrieves promises by category.

**Parameters**
- category: string (Core Inflation, Energy Costs, Tax Measures, Trade Policy, Housing Affordability)

#### POST /promises
Creates a new promise.

**Request Body**
```json
{
  "category": string,
  "text": string,
  "source": string,
  "source_link": string
}
```

#### PATCH /promises/{id}/status
Updates promise status.

**Request Body**
```json
{
  "status": "waiting" | "completed",
  "completion_date": string | null
}
```

#### GET /promises/stats
Retrieves promise completion statistics.

**Response**
```json
{
  "status": "Success",
  "stats": {
    "total": number,
    "completed": number,
    "waiting": number,
    "by_category": {
      "category_name": {
        "total": number,
        "completed": number,
        "waiting": number
      }
    }
  },
  "timestamp": string
}
```

## Database Schema

### fred_series
```sql
CREATE TABLE fred_series (
    series_id TEXT PRIMARY KEY,
    title TEXT,
    units TEXT,
    last_updated TIMESTAMP,
    latest_analysis TEXT,
    analysis_timestamp TIMESTAMP
);
```

### fred_data
```sql
CREATE TABLE fred_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    series_id TEXT,
    date TIMESTAMP,
    value REAL,
    FOREIGN KEY (series_id) REFERENCES fred_series(series_id)
);
```

### Planned Tables

#### promises
```sql
CREATE TABLE promises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    text TEXT NOT NULL,
    source TEXT NOT NULL,
    source_link TEXT NOT NULL,
    status TEXT DEFAULT 'waiting',
    completion_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### promise_history
```sql
CREATE TABLE promise_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    promise_id INTEGER,
    old_status TEXT,
    new_status TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (promise_id) REFERENCES promises(id)
);
```

## Error Handling

All endpoints return errors in the following format:

```json
{
  "status": "Error",
  "message": string,
  "error_code": string,
  "timestamp": string
}
```

Common error codes:
- `INVALID_REQUEST`: Invalid request parameters
- `NOT_FOUND`: Resource not found
- `RATE_LIMITED`: Too many requests
- `SERVER_ERROR`: Internal server error

## Rate Limiting
- 100 requests per minute per IP
- Rate limit headers included in response
- Exponential backoff recommended for retries
