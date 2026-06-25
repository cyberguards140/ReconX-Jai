"""Plugin schema definitions for ReconX plugin system."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PluginMetadata:
    """Metadata describing a plugin."""
    name: str
    version: str = "1.0.0"
    author: str = ""
    description: str = ""
    category: str = "Tool"
    capabilities: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    config_schema: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PluginResult:
    """Result returned after plugin execution."""
    plugin_name: str
    status: str = "success"
    output: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    assets: List[Dict[str, Any]] = field(default_factory=list)
    findings: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None
    execution_time: float = 0.0
