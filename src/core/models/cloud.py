from typing import Any

from pydantic import BaseModel, Field


class CloudAsset(BaseModel):
    provider: str  # e.g., 'aws', 'azure', 'gcp'
    service_type: str  # e.g., 's3_bucket', 'iam_role', 'load_balancer'
    identifier: str  # e.g., bucket name or ARN
    is_public: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)
    sources: list[str] = Field(default_factory=list)
