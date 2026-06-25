class ContainerGraphEngine:
    """
    Tracks container relationships and internal communication paths conceptually.
    """

    def __init__(self):
        self.edges = []

    def add_relationship(self, source_container: str, target_container: str, protocol: str):
        self.edges.append(
            {"source": source_container, "target": target_container, "protocol": protocol}
        )
