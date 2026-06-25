from sqlalchemy import func
from sqlalchemy.orm import Session

from data.database.models import Asset


class AnalyticsEngine:
    @staticmethod
    def get_attack_surface_overview(db: Session, project_id: str) -> dict:
        """
        Calculates the breakdown of assets for a given project.
        Returns counts for domains, subdomains, IPs, ports, and services.
        """
        # Get count of each asset_type
        counts = (
            db.query(Asset.asset_type, func.count(Asset.id))
            .filter(Asset.project_id == project_id, Asset.lifecycle_status != "retired")
            .group_by(Asset.asset_type)
            .all()
        )

        overview = {
            "domains": 0,
            "subdomains": 0,
            "ips": 0,
            "ports": 0,
            "services": 0,
            "cloud_assets": 0,
            "total_active": 0,
        }

        for asset_type, count in counts:
            normalized_type = asset_type.lower()
            if normalized_type in overview:
                overview[normalized_type] = count
            overview["total_active"] += count

        return overview

    @staticmethod
    def get_risk_trends(db: Session, project_id: str) -> dict:
        """
        Placeholder for historical risk trends calculation.
        """
        return {
            "critical_assets": db.query(Asset)
            .filter(Asset.project_id == project_id, Asset.confidence > 0.9)
            .count(),
            "new_this_week": 0,  # Would use created_at filtering
        }
