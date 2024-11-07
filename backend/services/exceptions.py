"""Custom exceptions for the inflation tracking service."""

class TrackerError(Exception):
    """Base exception for tracker errors."""
    pass

class ServiceInitializationError(TrackerError):
    """Error initializing services."""
    pass

class DataProcessingError(TrackerError):
    """Error processing data."""
    pass

class BackupError(TrackerError):
    """Error during backup operations."""
    pass
