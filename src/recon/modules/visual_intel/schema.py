from pydantic import BaseModel, Field


class VisualIntelModel(BaseModel):
    node_position: dict[str, float] = Field(default_factory=dict)
    cluster_id: str = ""
    visual_tags: list[str] = Field(default_factory=list)
    snapshot_ref: str = ""
    heat_level: int = 0


class TopologyZone(BaseModel):
    zone_name: str
    description: str
    member_asset_ids: list[str] = Field(default_factory=list)


class HeatMapSignal(BaseModel):
    asset_id: str
    heat_level: int
    color_code: str


class VisualCluster(BaseModel):
    cluster_id: str
    cluster_type: str
    member_asset_ids: list[str] = Field(default_factory=list)
