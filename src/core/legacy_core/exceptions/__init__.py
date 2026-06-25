"""Core exceptions package."""

from core.legacy_core.exceptions.errors import DnsError, HttpError, ValidationError

__all__ = ["ValidationError", "HttpError", "DnsError"]
