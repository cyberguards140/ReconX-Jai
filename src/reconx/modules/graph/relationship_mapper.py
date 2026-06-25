class RelationshipMapper:
    @staticmethod
    def map_ad_relationships(users: list, groups: list) -> list:
        edges = []
        for u in users:
            for g in u.get("groups", []):
                edges.append({"source": u["id"], "target": g, "type": "MEMBER_OF"})
        return edges

    @staticmethod
    def map_cloud_relationships(instances: list, vpcs: list) -> list:
        edges = []
        for i in instances:
            edges.append({"source": i["id"], "target": i["vpc_id"], "type": "BELONGS_TO"})
        return edges
        
    @staticmethod
    def map_network_relationships(domain: str, ip: str) -> list:
        return [{"source": domain, "target": ip, "type": "RESOLVES_TO"}]
