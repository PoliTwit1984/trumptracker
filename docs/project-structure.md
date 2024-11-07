# Project Structure

## Frontend Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard.jsx          # Main dashboard component with navigation
│   │   ├── InflationPromiseCard.jsx  # Card component for displaying inflation metrics
│   │   ├── PromiseMenu.jsx        # Navigation menu component
│   │   ├── PromiseTracker.jsx     # Campaign promises tracking component
│   │   └── PromiseCard.jsx        # Base promise card component
│   ├── App.jsx                    # Root application component
│   └── main.jsx                   # Application entry point
```

## Backend Structure

```
backend/
├── api/
│   └── routes.py                  # API endpoints
├── core/
│   ├── config.py                  # Configuration settings
│   ├── exceptions.py              # Custom exceptions
│   └── factory.py                 # Application factory
├── middleware/
│   └── security.py                # Security middleware
├── services/
│   ├── config.py                  # Service configurations
│   ├── data_analyzer.py           # Data analysis service using Claude
│   ├── data_fetcher.py           # FRED data fetching service
│   ├── decorators.py             # Service decorators
│   ├── exceptions.py             # Service exceptions
│   ├── inflation_tracker.py      # Main inflation tracking service
│   └── validators.py             # Data validation utilities
└── tests/                        # Test suite
```

## Database Structure

```
fred_data.db
├── fred_series                    # FRED series metadata and analysis
└── fred_data                      # Historical FRED data points
```

## TODOs

### High Priority
1. Move campaign promises to database
   - Create promises table with fields:
     - id
     - category
     - text
     - source
     - source_link
     - status (waiting/completed)
     - completion_date
   - Create API endpoints for promise management
   - Update PromiseTracker to fetch from API

2. Implement promise status persistence
   - Store checkbox states in database
   - Add API endpoints for status updates
   - Add timestamp for status changes

### Medium Priority
1. Add user authentication
   - Implement login system
   - Add role-based access control
   - Restrict promise status updates to admins

2. Add data visualization improvements
   - Add more detailed charts for metrics
   - Implement trend comparison views
   - Add export functionality for data

3. Enhance analysis features
   - Add historical analysis archive
   - Implement comparison between different time periods
   - Add custom date range selection

### Low Priority
1. Add notification system
   - Alert users of significant metric changes
   - Notify when promises are updated
   - Add email notification options

2. Implement caching
   - Cache API responses
   - Implement Redis for session management
   - Add browser caching headers

3. Add testing coverage
   - Add frontend component tests
   - Increase backend test coverage
   - Add integration tests

4. Documentation improvements
   - Add API documentation
   - Add developer setup guide
   - Create user manual
