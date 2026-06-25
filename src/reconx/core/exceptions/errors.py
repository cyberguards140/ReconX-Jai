"""Core exception classes for ReconX."""

from reconx.core.errors import ReconXError


class ValidationError(ReconXError):
    """Raised when input validation fails."""
    pass


class HttpError(ReconXError):
    """Raised when an HTTP operation fails."""
    pass


class DnsError(ReconXError):
    """Raised when a DNS operation fails."""
    pass
