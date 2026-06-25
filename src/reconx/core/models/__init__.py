"""Core data models for ReconX."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Asset:
    """Represents a discovered asset."""

    value: str
    asset_type: str = "unknown"
    source: str = "unknown"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AdapterResult:
    """Result returned by tool adapters after execution."""

    tool: str = ""
    target: str = ""
    status: str = "success"
    raw_output: str = ""
    assets: list[Asset] = field(default_factory=list)
    findings: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
