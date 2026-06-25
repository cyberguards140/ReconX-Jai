from pydantic import BaseModel, Field
from typing import Dict, List, Any

class CloudAssetModel(BaseModel):
    cloud_asset_id: str
    cloud_provider: str = "unknown"
    asset_type: str
    region: str = ""
    exposure_level: str = "Unknown Exposure"
    linked_assets: List[str] = Field(default_factory=list)

class K8sClusterData(BaseModel):
    cluster_name: str
    nodes: List[str] = Field(default_factory=list)
    namespaces: List[str] = Field(default_factory=list)
    pods: List[str] = Field(default_factory=list)
    services: List[str] = Field(default_factory=list)

class WorkloadModel(BaseModel):
    workload: str
    workload_type: str
    exposure: str
    dependencies: List[str] = Field(default_factory=list)

class ServiceMeshTraffic(BaseModel):
    source_service: str
    target_service: str
    protocol: str = "tcp"
