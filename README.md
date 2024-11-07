# Trump Tracker

A data-driven platform tracking economic promises and their outcomes through real-time Federal Reserve data and AI analysis.

## Documentation

The project documentation has been organized into separate files for better maintainability:

- [Project Overview](docs/overview.md)
- [Technology Stack](docs/tech-stack.md)
- [Project Structure](docs/project-structure.md)
- [Backend Architecture](docs/backend-architecture.md)
- [API Documentation](docs/api-docs.md)
- [Component Documentation](docs/components.md)
- [Setup Instructions](docs/setup.md)

## Recent Changes

### Backend Refactoring
The inflation tracking service has been refactored into smaller, more focused modules:

- **exceptions.py**: Custom exception definitions
- **decorators.py**: Utility decorators (e.g., retry mechanism)
- **validators.py**: Data validation functions
- **inflation_tracker.py**: Core service logic

This refactoring improves:
- Code maintainability
- Testing isolation
- Error handling clarity
- Module reusability

## Contributing

We welcome contributions! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
