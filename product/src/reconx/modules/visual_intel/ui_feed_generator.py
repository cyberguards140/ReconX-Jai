from typing import Dict, Any, List
from reconx.modules.visual_intel.schema import VisualIntelModel

class UIFeedGenerator:
    """
    Converts backend intelligence into real-time streams suitable for frontend dashboarding.
    """
    def __init__(self):
        pass

    def generate_dashboard_stream(self, asset_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Creates a JSON payload representing a live dashboard update.
        """
        return {
            "type": "dashboard_stream",
            "updates": asset_updates,
            "action": "refresh_nodes"
        }
