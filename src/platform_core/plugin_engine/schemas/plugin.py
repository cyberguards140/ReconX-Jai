"""Plugin schema definitions for ReconX plugin system."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PluginMetadata:
    """Metadata describing a plugin."""

    name: str
    version: str = "1.0.0"
    author: str = ""
    description: str = ""
    category: str = "Tool"
    capabilities: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)
    config_schema: dict[str, Any] = field(default_factory=dict)


@dataclass
class PluginResult:
    """Result returned after plugin execution."""

    plugin_name: str
    status: str = "success"
    output: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    assets: list[dict[str, Any]] = field(default_factory=list)
    findings: list[dict[str, Any]] = field(default_factory=list)
    error: str | None = None
    execution_time: float = 0.0
