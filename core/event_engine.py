from dashboard.backend.websocket import broadcast

class EventEngine:
    @staticmethod
    def publish_new_asset(asset_type, value, project_id, source):
        msg = {
            "type": "new_asset",
            "asset_type": asset_type,
            "value": value,
            "project_id": project_id,
            "source": source
        }
        broadcast(msg)

    @staticmethod
    def publish_asset_updated(asset_type, value, project_id, source):
        msg = {
            "type": "asset_updated",
            "asset_type": asset_type,
            "value": value,
            "project_id": project_id,
            "source": source
        }
        broadcast(msg)
