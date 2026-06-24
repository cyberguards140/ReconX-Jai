class RelationshipEngine:
    @staticmethod
    def get_valid_edges(source_type: str) -> list[str]:
        ontology = {
            "Domain": ["RESOLVES_TO"],
            "IP": ["HOSTS"],
            "Service": ["RUNS"],
            "User": ["MEMBER_OF"],
            "CloudInstance": ["BELONGS_TO"],
            "Asset": ["AFFECTED_BY"]
        }
        return ontology.get(source_type, [])
