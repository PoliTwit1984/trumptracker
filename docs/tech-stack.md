# Technology Stack

## Backend

### Core
- **Python 3.8+**: Main programming language
- **Flask**: Web framework
- **SQLite**: Database
- **SQLAlchemy**: ORM and database toolkit

### APIs
- **FRED API**: Federal Reserve Economic Data
- **Claude API**: AI analysis via Anthropic

### Libraries
- **fredapi**: FRED API client
- **anthropic**: Claude API client
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **flask-limiter**: Rate limiting
- **flask-cors**: CORS handling
- **python-dotenv**: Environment variable management
- **pytest**: Testing framework
- **logging**: Built-in logging

## Frontend

### Core
- **React**: UI framework
- **Vite**: Build tool and development server
- **JavaScript/ES6+**: Programming language

### UI Components
- **Material-UI (MUI)**: Component library
- **Recharts**: Charting library

### State Management
- **React Hooks**: Local state management
- **useEffect**: Side effect handling
- **useCallback**: Performance optimization

### HTTP Client
- **Axios**: HTTP requests

### Development Tools
- **ESLint**: Code linting
- **PropTypes**: Runtime type checking

## Development Tools

### Version Control
- **Git**: Source control
- **GitHub**: Repository hosting

### IDE
- **VSCode**: Primary development environment
  - ESLint extension
  - Python extension
  - Git extension
  - React extension

### Testing
- **pytest**: Backend testing
- **pytest-cov**: Test coverage
- **React Testing Library**: Frontend testing (planned)

### Documentation
- **Markdown**: Documentation format
- **JSDoc**: JavaScript documentation

## Infrastructure

### Database
- **SQLite**: Local database
- **SQLAlchemy**: Database ORM
- **Alembic**: Database migrations (planned)

### Caching
- **In-memory caching**: API response caching
- **SQLite**: Data persistence

### Monitoring (Planned)
- **Logging**: Application logging
- **Metrics**: Performance monitoring
- **Alerts**: Error alerting
- **Health checks**: Service health monitoring

## To Do

### Backend
1. Add database migrations with Alembic
2. Add Celery for background tasks
3. Add Redis for caching
4. Add Prometheus for metrics
5. Add Grafana for monitoring
6. Add Sentry for error tracking
7. Add OpenAPI/Swagger for API docs
8. Add JWT for authentication
9. Add pytest-asyncio for async testing
10. Add mypy for static typing

### Frontend
1. Add TypeScript
2. Add React Testing Library
3. Add Cypress for E2E testing
4. Add Redux for state management
5. Add Storybook for component docs
6. Add React Query for data fetching
7. Add React Router for routing
8. Add React Error Boundary
9. Add PWA support
10. Add service workers

### Infrastructure
1. Add Docker containerization
2. Add Kubernetes orchestration
3. Add CI/CD pipeline
4. Add automated deployments
5. Add infrastructure as code
6. Add security scanning
7. Add performance monitoring
8. Add load balancing
9. Add CDN integration
10. Add backup solution
