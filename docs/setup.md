# Setup Instructions

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

### Testing
```bash
# Run backend tests
cd backend
python -m pytest

# Run frontend tests
cd frontend
npm test
