from pydantic import BaseModel, Field


class CloudAssetModel(BaseModel):
    cloud_asset_id: str
    cloud_provider: str = "unknown"
    asset_type: str
    region: str = ""
    exposure_level: str = "Unknown Exposure"
    linked_assets: list[str] = Field(default_factory=list)


class K8sClusterData(BaseModel):
    cluster_name: str
    nodes: list[str] = Field(default_factory=list)
    namespaces: list[str] = Field(default_factory=list)
    pods: list[str] = Field(default_factory=list)
    services: list[str] = Field(default_factory=list)


class WorkloadModel(BaseModel):
    workload: str
    workload_type: str
    exposure: str
    dependencies: list[str] = Field(default_factory=list)


class ServiceMeshTraffic(BaseModel):
    source_service: str
    target_service: str
    protocol: str = "tcp"
