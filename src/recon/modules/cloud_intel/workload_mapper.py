from recon.modules.cloud_intel.schema import WorkloadModel


class WorkloadMapper:
    """
    Maps logical applications, APIs, and microservices to dependencies.
    """

    def __init__(self):
        pass

    def map_workload(self, name: str, workload_type: str, dependencies: list) -> WorkloadModel:
        """
        Abstract workload representation mapping.
        """
        exposure = "Internal Cloud Exposure"
        if workload_type == "api_gateway":
            exposure = "Public Cloud Exposure"

        return WorkloadModel(
            workload=name, workload_type=workload_type, exposure=exposure, dependencies=dependencies
        )
