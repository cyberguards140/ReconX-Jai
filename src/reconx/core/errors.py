"""Core error classes for ReconX."""


class ReconXError(Exception):
    """Base exception for all ReconX errors."""
    pass


class ConfigurationError(ReconXError):
    """Raised when configuration is invalid or missing."""
    pass
