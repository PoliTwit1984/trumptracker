# Setup Guide

## Prerequisites

### Required Software
- Python 3.8 or higher
- Node.js 16 or higher
- npm 8 or higher
- Git
- VSCode (recommended)

### API Keys
- FRED API key from [Federal Reserve Economic Data](https://fred.stlouisfed.org/docs/api/api_key.html)
- Claude API key from [Anthropic](https://anthropic.com/)

## Environment Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/trumptracker.git
cd trumptracker
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Environment Variables
Create a `.env` file in the root directory:
```env
FRED_API_KEY=your_fred_api_key
ANTHROPIC_API_KEY=your_claude_api_key
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

#### Initialize Database
```bash
# Start the Flask server
python -m backend.app

# In another terminal, initialize the database
curl -X POST http://localhost:5003/api/v1/inflation/initialize
```

### 3. Frontend Setup

#### Install Dependencies
```bash
cd frontend
npm install
```

## Running the Application

### Start Backend Server
```bash
# From project root
python -m backend.app
```
Backend will be available at `http://localhost:5003`

### Start Frontend Development Server
```bash
# From frontend directory
npm run dev
```
Frontend will be available at `http://localhost:5173`

## Development

### Backend Development
- API endpoints are in `backend/api/routes.py`
- Database models are in `backend/database.py`
- Services are in `backend/services/`
- Tests are in `backend/tests/`

### Frontend Development
- Components are in `frontend/src/components/`
- Styles are in `frontend/src/`
- Assets are in `frontend/src/assets/`

## Testing

### Backend Tests
```bash
# From project root
pytest backend/tests/
```

### Frontend Tests (Planned)
```bash
# From frontend directory
npm test
```

## Common Issues

### Database Issues
If you encounter database issues:
1. Delete the `fred_data.db` file
2. Restart the backend server
3. Re-initialize the database

### Rate Limiting
- FRED API has a rate limit of 120 requests per minute
- Claude API has rate limiting based on your plan
- Backend implements rate limiting of 5 requests per second

### Cache Issues
If you encounter stale data:
1. Clear the browser cache
2. Restart the backend server
3. Re-initialize the database

## To Do

### Backend Setup
1. Add database migration commands
2. Add automated database backup
3. Add development/production configs
4. Add logging configuration
5. Add monitoring setup

### Frontend Setup
1. Add TypeScript configuration
2. Add testing setup
3. Add storybook setup
4. Add PWA configuration
5. Add production build setup

### Development Tools
1. Add pre-commit hooks
2. Add code formatting tools
3. Add automated testing
4. Add CI/CD pipeline
5. Add deployment scripts
