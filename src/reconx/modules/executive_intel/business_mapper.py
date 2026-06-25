import uuid

from reconx.modules.executive_intel.schema import BusinessServiceModel


class BusinessMapper:
    """
    Links technical assets to business services and units.
    """

    def __init__(self):
        self.services = {}

    def map_service(self, name: str, criticality: str, assets: list[str]) -> BusinessServiceModel:
        svc = BusinessServiceModel(
            service_id=f"svc_{uuid.uuid4().hex[:8]}",
            service_name=name,
            criticality=criticality,
            linked_assets=assets,
        )
        self.services[svc.service_id] = svc
        return svc
