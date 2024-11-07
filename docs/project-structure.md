# Project Structure

```
trumptracker/
├── backend/
│   ├── app.py                 # Flask server and API endpoints
│   ├── fred_api.py           # Compatibility wrapper for services
│   ├── database.py           # Database models and operations
│   └── services/             # Modular service components
│       ├── __init__.py       # Service package exports
│       ├── config.py         # Configuration and constants
│       ├── data_fetcher.py   # FRED data fetching service
│       ├── data_analyzer.py  # Claude AI analysis service
│       ├── inflation_tracker.py # Main service coordinator
│       ├── exceptions.py     # Custom exception definitions
│       ├── decorators.py     # Utility decorators (e.g., retry)
│       └── validators.py     # Data validation functions
│   └── tests/               # Test suite
│       ├── conftest.py      # Test configuration and fixtures
│       ├── test_app.py      # API endpoint tests
│       ├── test_data_analyzer.py # AI analysis tests
│       ├── test_data_fetcher.py # FRED data tests
│       └── test_inflation_tracker.py # Service tests
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
└── docs/                    # Project documentation
    ├── overview.md          # Project overview and features
    ├── tech-stack.md        # Technology stack details
    ├── backend-architecture.md # Backend design and components
    ├── project-structure.md # Directory structure
    ├── api-docs.md         # API documentation
    ├── components.md       # Frontend component docs
    └── setup.md           # Setup instructions
