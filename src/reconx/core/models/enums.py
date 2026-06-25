"""Core model enumerations for ReconX."""

from enum import Enum


class AssetType(str, Enum):
    """Enumeration of recognized asset types."""

    DOMAIN = "DOMAIN"
    SUBDOMAIN = "SUBDOMAIN"
    IP = "IP"
    URL = "URL"
    ENDPOINT = "ENDPOINT"
    PORT = "PORT"
    SERVICE = "SERVICE"
    TECHNOLOGY = "TECHNOLOGY"
    CERTIFICATE = "CERTIFICATE"
    EMAIL = "EMAIL"
    ASN = "ASN"
    CIDR = "CIDR"
    CLOUD_RESOURCE = "CLOUD_RESOURCE"
    CONTAINER = "CONTAINER"
    API = "API"
    SECRET = "SECRET"
    REPOSITORY = "REPOSITORY"
    UNKNOWN = "UNKNOWN"
