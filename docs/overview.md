# Trump Tracker Overview

## Project Purpose
Trump Tracker is a comprehensive platform designed to monitor and analyze economic metrics and campaign promises related to inflation and economic policies. The system provides real-time tracking of key economic indicators while maintaining a record of related campaign promises and their fulfillment status.

## Core Features

### Inflation Metrics Dashboard
- Real-time tracking of key economic indicators
- Interactive data visualization
- AI-powered analysis using Claude
- Historical data comparison
- Regular data updates from FRED API

### Campaign Promise Tracker
- Categorized promise listing
- Status tracking with visual indicators
- Source verification links
- Progress monitoring
- Historical record keeping

## System Architecture

### Frontend
- React-based single-page application
- Material-UI components for consistent design
- Responsive layout for all devices
- Real-time data updates
- Interactive data visualization

### Backend
- Flask-based REST API
- FRED API integration
- Claude AI integration for analysis
- SQLite database for data storage
- Automated data updates

## Current Implementation

### Metrics Tracking
- Consumer Price Index (CPI)
- Core CPI (excluding food and energy)
- Food Price Index
- Gas Prices
- Housing Price Index

### Promise Categories
- Core Inflation Promises
- Energy Costs
- Tax Measures
- Trade Policy
- Housing Affordability

### UI Features
- Expandable metric cards with detailed analysis
- Interactive charts and visualizations
- Status indicators for promises
- Source verification links
- Category-based organization

## Planned Enhancements

### Database Migration
1. Campaign Promises Storage
   - Move promises from static file to database
   - Implement CRUD operations
   - Add status change tracking
   - Enable dynamic updates

### Feature Additions
1. User Management
   - Authentication system
   - Role-based access control
   - Admin dashboard
   - User preferences

2. Enhanced Analytics
   - Comparative analysis tools
   - Custom date ranges
   - Trend predictions
   - Export capabilities

3. Notification System
   - Status change alerts
   - Metric threshold notifications
   - Email updates
   - Custom alert settings

### Technical Improvements
1. Performance
   - Implement caching
   - Optimize data fetching
   - Add lazy loading
   - Improve response times

2. Testing
   - Expand test coverage
   - Add integration tests
   - Implement E2E testing
   - Performance testing

3. Documentation
   - API documentation
   - User guides
   - Development guides
   - Deployment documentation

## Getting Started

### Prerequisites
- Node.js 16+
- Python 3.8+
- SQLite 3

### Environment Setup
1. Clone repository
2. Install dependencies
3. Set up environment variables
4. Initialize database
5. Start development servers

### Development Workflow
1. Frontend development (Vite + React)
2. Backend development (Flask)
3. Database management (SQLite)
4. Testing and validation
5. Documentation updates

## Contributing
- Fork repository
- Create feature branch
- Submit pull request
- Follow coding standards
- Include tests
- Update documentation

## License
MIT License - See LICENSE file for details
