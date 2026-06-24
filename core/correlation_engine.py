from core.inventory_manager import InventoryManager

class CorrelationEngine:
    @staticmethod
    def process_normalized_asset(normalized_data, project_id, source):
        """
        normalized_data shape:
        {
            "type": "subdomain",
            "value": "api.example.com",
            "related": [
                {"type": "ip", "value": "1.2.3.4", "relation": "resolves_to"},
                {"type": "port", "value": "443", "relation": "has_port"}
            ]
        }
        """
        if not project_id:
            return

        main_type = normalized_data.get("type")
        main_value = normalized_data.get("value")
        
        if not main_type or not main_value:
            return
            
        main_id, is_new = InventoryManager.get_or_create_asset(main_type, main_value, project_id, source)
        
        related = normalized_data.get("related", [])
        for rel in related:
            r_type = rel.get("type")
            r_value = rel.get("value")
            r_rel = rel.get("relation", "linked")
            
            if r_type and r_value:
                r_id, _ = InventoryManager.get_or_create_asset(r_type, r_value, project_id, source)
                InventoryManager.create_relationship(main_id, r_id, r_rel)
