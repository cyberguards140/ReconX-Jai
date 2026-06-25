"""Core data models for ReconX."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class Asset:
    """Represents a discovered asset."""
    value: str
    asset_type: str = "unknown"
    source: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AdapterResult:
    """Result returned by tool adapters after execution."""
    tool: str = ""
    target: str = ""
    status: str = "success"
    raw_output: str = ""
    assets: List[Asset] = field(default_factory=list)
    findings: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
