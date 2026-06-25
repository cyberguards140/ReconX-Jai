from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any, List
from reconx.database.repositories.asset import asset_repo, asset_history_repo, asset_rel_repo
from reconx.services.intelligence.deduplicator import Deduplicator
from reconx.services.intelligence.relationship_engine import RelationshipEngine
from reconx.services.intelligence.asset_correlator import AssetCorrelator


from reconx.services.intelligence.schemas import AssetSchema
from pydantic import ValidationError

class IntelligenceStore:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def ingest_plugin_result(self, project_id: str, results: Dict[str, Any]):
        # Pipeline: Normalizer -> Deduplicator -> Relationship -> Intelligence Store
        raw_assets = results.get("assets", [])
        raw_findings = results.get("findings", [])

        normalized_assets = []
        for a in raw_assets:
            try:
                asset = AssetSchema(
                    asset_type=a.get("type", a.get("asset_type", "DOMAIN")).upper(),
                    value=a.get("value", ""),
                    source=a.get("source", "unknown"),
                    project_id=project_id,
                )
                normalized_assets.append(asset.model_dump())
            except ValidationError as e:
                # Log invalid asset (silently ignore for now as per legacy behavior)
                continue

        deduped_assets = Deduplicator.deduplicate_assets(normalized_assets)

        # Save assets
        asset_id_map = {}
        for a in deduped_assets:
            # check if exists
            existing = await asset_repo.get_by_value(self.db, project_id, a["asset_type"], a["value"])
            if not existing:
                new_asset = await asset_repo.create(self.db, obj_in={
                    "project_id": project_id,
                    "asset_type": a["asset_type"],
                    "value": a["value"],
                    "source": a["source"],
                })
                asset_id_map[a["value"]] = new_asset.id
                await asset_history_repo.create(self.db, obj_in={"asset_id": new_asset.id, "event": "Discovered"})
            else:
                asset_id_map[a["value"]] = existing.id
                await asset_history_repo.create(self.db, obj_in={"asset_id": existing.id, "event": f"Seen again via {a['source']}"})

        # Relationships
        rels = RelationshipEngine.infer_parent_child(deduped_assets)
        for r in rels:
            p_id = asset_id_map.get(r["parent_value"])
            c_id = asset_id_map.get(r["child_value"])
            if p_id and c_id:
                # check existing
                existing_rel = await asset_rel_repo.get_relationship(self.db, p_id, c_id)
                if not existing_rel:
                    await asset_rel_repo.create(self.db, obj_in={
                        "parent_asset_id": p_id,
                        "child_asset_id": c_id,
                        "relationship_type": r["relationship_type"],
                    })

        # Findings
        deduped_findings = Deduplicator.deduplicate_findings(raw_findings)
        correlated = AssetCorrelator.correlate_findings(deduped_findings)

        for f in correlated:
            # We assume finding has scan_id injected by workflow context, but for simplicity we will just store intelligence record
            # In a full flow, findings attach to scans. We will attach them to IntelligenceRecord for the asset if asset matches.
            pass

        # Flush the intelligence changes. The caller (e.g. state_manager) will call transaction's commit.
        await self.db.flush()

    async def get_assets(self) -> List[Dict[str, Any]]:
        assets = await asset_repo.get_multi(self.db)
        return [
            {"id": a.id, "type": a.asset_type, "value": a.value, "source": a.source}
            for a in assets
        ]

    async def get_asset_graph(self) -> Dict[str, Any]:
        assets_list = await asset_repo.get_multi(self.db)
        assets = {a.id: a for a in assets_list}

        rels = await asset_rel_repo.get_multi(self.db)

        graph = {
            "nodes": [
                {"id": a.id, "value": a.value, "type": a.asset_type}
                for a in assets.values()
            ],
            "edges": [
                {
                    "source": r.parent_asset_id,
                    "target": r.child_asset_id,
                    "type": r.relationship_type,
                }
                for r in rels
            ],
        }
        return graph
