from recon.modules.cloud_intel.schema import ServiceMeshTraffic


class ServiceMeshMapper:
    """
    Models internal traffic routing and service dependencies within a cluster.
    """

    def __init__(self):
        self.routes = []

    def record_traffic(self, source: str, target: str, protocol: str) -> ServiceMeshTraffic:
        traffic = ServiceMeshTraffic(
            source_service=source, target_service=target, protocol=protocol
        )
        self.routes.append(traffic)
        return traffic
