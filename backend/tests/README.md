# Trump Tracker Tests

## Overview

This directory contains comprehensive tests for the Trump Tracker backend services. The test suite covers:

- Unit tests for individual components
- Integration tests for service interactions
- API endpoint tests
- Error handling and validation tests
- Rate limiting tests
- Security tests

## Test Structure

```
tests/
├── README.md           # This file
├── conftest.py        # Shared test fixtures and configuration
├── test_app.py        # Tests for Flask application endpoints
├── test_data_analyzer.py    # Tests for AI analysis service
├── test_data_fetcher.py     # Tests for FRED data fetching service
└── test_inflation_tracker.py # Tests for main service coordinator
```

## Setup

1. Install test dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export FRED_API_KEY=your_fred_api_key
export ANTHROPIC_API_KEY=your_claude_api_key
export CLAUDE_MODEL=claude-3-opus-20240229
```

## Running Tests

### Run all tests:
```bash
pytest
```

### Run with coverage report:
```bash
pytest --cov
```

### Run specific test files:
```bash
pytest tests/test_app.py
pytest tests/test_data_fetcher.py
pytest tests/test_data_analyzer.py
pytest tests/test_inflation_tracker.py
```

### Run tests by marker:
```bash
pytest -m unit          # Run unit tests only
pytest -m integration   # Run integration tests only
pytest -m "not slow"    # Skip slow tests
```

## Coverage Reports

- Terminal report: Shows coverage statistics in the terminal
- HTML report: Generated in `coverage_html/` directory
  - Open `coverage_html/index.html` in a browser to view

## Test Categories

### Unit Tests
- Individual component testing
- Mocked dependencies
- Fast execution

### Integration Tests
- Service interaction testing
- Database operations
- API integrations

### API Tests
- Endpoint functionality
- Request/response validation
- Error handling
- Rate limiting
- Security headers

## Key Test Areas

### Data Fetcher Service
- FRED API interaction
- Data validation
- Error handling
- Retry mechanism
- Rate limiting

### Data Analyzer Service
- Claude AI integration
- Prompt generation
- Analysis validation
- Error handling
- Rate limiting

### Inflation Tracker Service
- Service coordination
- Status tracking
- Error propagation
- Backup operations

### Flask Application
- API endpoints
- Request validation
- Error handling
- Security headers
- Rate limiting
- Logging

## Fixtures

Common test fixtures are defined in `conftest.py`:
- Mock environment variables
- Sample metrics data
- Mock database session
- Mock API responses
- Mock logger

## Configuration

### pytest.ini
- Test discovery settings
- Logging configuration
- Coverage settings
- Test markers
- Warning filters
- Timeout settings

### .coveragerc
- Coverage measurement configuration
- Report settings
- Exclusion patterns
- Coverage thresholds

## Best Practices

1. **Test Independence**
   - Each test should be independent
   - Use fixtures for setup/teardown
   - Avoid test interdependencies

2. **Mocking**
   - Mock external services
   - Use appropriate scope for mocks
   - Verify mock interactions

3. **Assertions**
   - Use specific assertions
   - Check both positive and negative cases
   - Validate error conditions

4. **Coverage**
   - Maintain high coverage (>90%)
   - Focus on critical paths
   - Include edge cases

5. **Documentation**
   - Document test purpose
   - Explain complex test scenarios
   - Keep documentation updated

## Maintenance

1. **Regular Updates**
   - Keep dependencies updated
   - Review and update tests for new features
   - Maintain test documentation

2. **Performance**
   - Monitor test execution time
   - Mark slow tests appropriately
   - Consider parallel execution

3. **Quality Checks**
   - Run tests before commits
   - Maintain coverage thresholds
   - Review test logs regularly

## Troubleshooting

### Common Issues

1. **Environment Variables**
   - Ensure all required variables are set
   - Check variable format
   - Verify API keys are valid

2. **Database Tests**
   - Check mock session configuration
   - Verify transaction handling
   - Ensure proper cleanup

3. **API Tests**
   - Check rate limiting configuration
   - Verify endpoint URLs
   - Validate request formats

### Debug Tips

1. Enable verbose output:
```bash
pytest -vv
```

2. Show print statements:
```bash
pytest -s
```

3. Debug specific test:
```bash
pytest tests/test_file.py::TestClass::test_name -vv
```

## Contributing

1. Follow existing test patterns
2. Add appropriate markers
3. Include documentation
4. Maintain coverage standards
5. Add to this README as needed
