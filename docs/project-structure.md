# Project Structure

## Backend

### Core (`backend/core/`)
- `config.py`: Application configuration and environment variables
- `exceptions.py`: Custom exception classes
- `factory.py`: Flask application factory

### API (`backend/api/`)
- `routes.py`: API endpoint definitions and handlers

### Services (`backend/services/`)
- `data_fetcher.py`: FRED API interaction and data retrieval
- `data_analyzer.py`: AI analysis using Claude API
- `inflation_tracker.py`: Main business logic
- `config.py`: Service-specific configuration
- `decorators.py`: Service utility decorators
- `validators.py`: Data validation utilities
- `exceptions.py`: Service-specific exceptions

### Database
- `database.py`: Database models and utilities
- `fred_data.db`: SQLite database file

### Tests (`backend/tests/`)
- `conftest.py`: Test configuration
- `test_app.py`: API tests
- `test_data_analyzer.py`: Analysis service tests
- `test_data_fetcher.py`: Data fetcher tests
- `test_inflation_tracker.py`: Business logic tests

### Middleware (`backend/middleware/`)
- `security.py`: Security middleware and request logging

## Frontend

### Components (`frontend/src/components/`)
- `Dashboard.jsx`: Main dashboard component
- `InflationPromiseCard.jsx`: Individual metric display
- `PromiseMenu.jsx`: Navigation menu

### Assets (`frontend/src/assets/`)
- Static assets and images

### Styles (`frontend/src/`)
- `App.css`: Application styles
- `index.css`: Global styles

### Configuration
- `vite.config.js`: Vite configuration
- `package.json`: Dependencies and scripts
- `eslint.config.js`: ESLint configuration

## Documentation (`docs/`)
- `overview.md`: Project overview and status
- `backend-architecture.md`: Backend architecture details
- `api-docs.md`: API documentation
- `setup.md`: Setup instructions
- `tech-stack.md`: Technology stack details
- `project-structure.md`: This file
- `components.md`: Frontend component documentation

## Root Files
- `.gitignore`: Git ignore rules
- `requirements.txt`: Python dependencies
- `README.md`: Project readme
- `promise.md`: Promise tracking documentation

## To Do
1. Add frontend testing directory
2. Add frontend state management
3. Add frontend error boundary components
4. Add frontend service layer
5. Add frontend type definitions
6. Add frontend documentation
7. Add backend API versioning
8. Add backend database migrations
9. Add backend job scheduling
10. Add deployment configuration
11. Add monitoring configuration
12. Add CI/CD configuration
