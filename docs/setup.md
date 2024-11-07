# Setup Instructions

## Prerequisites
- Python 3.12+
- Node.js 18+
- FRED API key
- Anthropic API key

## Backend Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FRED_API_KEY=your_fred_api_key
export ANTHROPIC_API_KEY=your_claude_api_key

# Start the server
cd backend
python app.py
```

## Frontend Setup
```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm run dev
```

## Development Notes

### Environment Variables
- FRED_API_KEY: Required for accessing Federal Reserve Economic Data
- ANTHROPIC_API_KEY: Required for AI analysis features

### Development Server
- Backend runs on http://localhost:5000
- Frontend runs on http://localhost:3000
- API endpoints are CORS-enabled for development

### Running Tests
```bash
# Run all backend tests with coverage
cd backend
python -m pytest --cov=services tests/

# Run specific test modules
python -m pytest tests/test_inflation_tracker.py -v
python -m pytest tests/test_data_analyzer.py -v
python -m pytest tests/test_data_fetcher.py -v

# Run frontend tests
cd frontend
npm test
```

### Test Coverage
Current coverage by module:
- decorators.py: 81.82%
- validators.py: 86.84%
- data_analyzer.py: 15.18%
- data_fetcher.py: 13.22%
- Overall: 34.97%

Target coverage: 80%

### Code Organization
```
backend/
├── services/           # Core service modules
│   ├── config.py      # Configuration
│   ├── data_fetcher.py # FRED integration
│   ├── data_analyzer.py # AI analysis
│   ├── inflation_tracker.py # Service coordinator
│   ├── exceptions.py  # Custom exceptions
│   ├── decorators.py  # Utility decorators
│   └── validators.py  # Data validation
└── tests/            # Test suite
```

### Development Workflow
1. Activate virtual environment
2. Run tests before making changes
3. Make code changes
4. Run tests again to verify
5. Check test coverage
6. Update documentation if needed

### Common Issues
- Import errors in tests: Make sure you're running from the correct directory
- Missing API keys: Check environment variables
- Test failures: Check mock configurations
- Coverage below target: Add missing test cases

### Best Practices
- Run tests frequently during development
- Keep test coverage high
- Update documentation with changes
- Follow modular service architecture
- Use proper error handling
- Validate all inputs
- Write comprehensive tests

### Troubleshooting
- Check environment variables are set
- Verify virtual environment is active
- Ensure all dependencies are installed
- Check test fixtures are properly configured
- Verify mock objects are set up correctly
- Review error messages carefully
