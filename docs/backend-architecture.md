# Backend Architecture

## Core Components

### Database Layer
- SQLite database for storing FRED economic data
- Tables:
  - `fred_series`: Stores metadata about economic indicators
  - `fred_data`: Stores historical data points for each series
- Indexes for optimized querying
- Connection pooling for better performance
- Data is updated on different schedules:
  - Weekly: Gas prices
  - Monthly: CPI, Core CPI, Food Index, Housing Index

### Data Management
- Data is primarily served from local database
- FRED API is only called during scheduled updates
- Update frequency varies by metric type
- Historical data is preserved for trend analysis
- Data validation ensures consistency

### Data Fetching
- `FREDDataFetcher` class handles all FRED API interactions
- Only fetches new data during scheduled updates
- Validates and transforms data before storage
- Handles rate limiting and retries
- Implements exponential backoff for failed requests

### Data Analysis
- `InflationAnalyzer` class handles AI-powered analysis
- Uses Claude API for trend analysis
- Implements caching to reduce API costs
- Validates and sanitizes analysis results
- Handles rate limiting gracefully

### API Layer
- Flask-based REST API
- Endpoints:
  - `/api/v1/inflation/data`: Get current inflation metrics (from database)
  - `/api/v1/inflation/initialize`: Initialize historical data
  - `/api/v1/inflation/update`: Update with latest data (scheduled)
  - `/api/v1/inflation/backup`: Create database backup
  - `/api/v1/health`: Health check endpoint
- Implements proper error handling
- Includes request validation
- Logs all requests for debugging

## Data Flow
1. Frontend requests data from API
2. API layer validates request
3. Data fetcher retrieves data from local database
4. During scheduled updates:
   - Check FRED API for new data
   - If new data exists, fetch and store in database
   - Update metadata and timestamps
5. Get AI analysis (cached if available)
6. Return combined data to frontend

## Update Schedule
- Gas Prices:
  - Update frequency: Weekly
  - Source: FRED GASREGW series
  - Update day: Monday
- CPI Metrics:
  - Update frequency: Monthly
  - Source: FRED CPIAUCSL, CPILFESL, CPIUFDSL series
  - Update day: 15th of each month
- Housing Index:
  - Update frequency: Monthly
  - Source: FRED CSUSHPISA series
  - Update day: Last day of month

## Error Handling
- Custom exception classes for different error types
- Proper error logging
- Graceful degradation
- User-friendly error messages
- Retry mechanisms for transient failures

## Caching Strategy
- Database as primary data store
- In-memory caching for AI analysis
- Cache invalidation based on data freshness
- Cache bypass for forced updates

## Security
- Input validation
- Rate limiting
- Request logging
- Error sanitization
- CORS configuration

## Monitoring
- Detailed logging throughout the application
- Performance metrics logging
- Error tracking
- API usage monitoring
- Data freshness monitoring

## To Do
1. Implement automated update scheduling
2. Add data freshness monitoring
3. Implement database backup functionality
4. Add data versioning
5. Implement user authentication
6. Add admin endpoints for data management
7. Implement automated testing
8. Add monitoring alerts
9. Implement rate limiting for public endpoints
10. Add data export functionality
11. Implement automated deployments
12. Add health check monitoring
