from reconx.modules.cloud_intel.schema import K8sClusterData


class K8sClusterEngine:
    """
    Abstracts Kubernetes hierarchies: Cluster -> Namespace -> Pod -> Service
    """

    def __init__(self):
        pass

    def build_cluster_model(self, name: str, data: dict) -> K8sClusterData:
        return K8sClusterData(
            cluster_name=name,
            nodes=data.get("nodes", []),
            namespaces=data.get("namespaces", []),
            pods=data.get("pods", []),
            services=data.get("services", []),
        )
