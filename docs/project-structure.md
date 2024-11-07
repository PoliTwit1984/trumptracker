# Project Structure

```
trumptracker/
├── backend/
│   ├── app.py                 # Flask server and API endpoints
│   ├── fred_api.py           # FRED API wrapper
│   ├── database.py           # Database models and operations
│   ├── services/             # Modular service components
│   │   ├── __init__.py       # Service package exports
│   │   ├── config.py         # Configuration and constants
│   │   ├── data_fetcher.py   # FRED data fetching (13.22% coverage)
│   │   ├── data_analyzer.py  # Claude AI analysis (15.18% coverage)
│   │   ├── inflation_tracker.py # Service coordinator
│   │   ├── exceptions.py     # Custom exception definitions
│   │   ├── decorators.py     # Utility decorators (81.82% coverage)
│   │   └── validators.py     # Data validation (86.84% coverage)
│   ├── tests/               # Test suite
│   │   ├── conftest.py      # Test configuration and fixtures
│   │   ├── test_app.py      # API endpoint tests
│   │   ├── test_data_analyzer.py # AI analysis tests
│   │   ├── test_data_fetcher.py # FRED data tests
│   │   └── test_inflation_tracker.py # Service tests
│   └── .coveragerc          # Coverage configuration
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx      # Main dashboard layout
│   │   │   ├── PromiseMenu.jsx    # Navigation menu component
│   │   │   ├── PromiseCard.jsx    # Generic promise display
│   │   │   └── InflationPromiseCard.jsx # Economic indicator cards
│   │   ├── App.jsx           # Root component
│   │   └── index.css         # Global styles
│   ├── package.json          # Frontend dependencies
│   └── vite.config.js        # Vite configuration
├── docs/                    # Project documentation
│   ├── overview.md          # Project overview and features
│   ├── tech-stack.md        # Technology stack details
│   ├── backend-architecture.md # Backend design and components
│   ├── project-structure.md # Directory structure
│   ├── api-docs.md         # API documentation
│   ├── components.md       # Frontend component docs
│   └── setup.md           # Setup instructions
└── README.md               # Project documentation
```

## Key Features

### Backend Organization
- Modular service architecture
- Clear separation of concerns
- Comprehensive test coverage
- Isolated components
- Centralized configuration
- Custom error handling
- Utility functions
- Data validation

### Frontend Structure
- Component-based architecture
- Reusable UI elements
- Centralized state management
- Consistent styling
- Error handling
- Loading states
- Data visualization

### Documentation
- Comprehensive guides
- API documentation
- Setup instructions
- Architecture overview
- Component documentation
- Testing guidelines

### Testing
- Unit tests
- Integration tests
- Test fixtures
- Mock objects
- Coverage reporting
- Automated testing
- Test configuration

## Module Descriptions

### Backend Services
- **config.py**: Configuration management and constants
- **data_fetcher.py**: FRED API integration and data management
- **data_analyzer.py**: AI-powered economic analysis
- **inflation_tracker.py**: Service coordination and orchestration
- **exceptions.py**: Custom error handling
- **decorators.py**: Utility decorators and function wrappers
- **validators.py**: Data validation and verification

### Frontend Components
- **Dashboard.jsx**: Main application layout
- **PromiseMenu.jsx**: Navigation and filtering
- **PromiseCard.jsx**: Generic promise display
- **InflationPromiseCard.jsx**: Economic data visualization

### Documentation
- Organized by topic
- Regular updates
- Clear structure
- Comprehensive coverage
