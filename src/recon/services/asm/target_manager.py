import uuid

from pydantic import BaseModel


class Target(BaseModel):
    id: str
    domain: str
    scope: list[str]
    scan_policy: str = "continuous"


class TargetManager:
    def __init__(self):
        self.targets = {}

    def add_target(
        self, domain: str, scope: list[str] = None, scan_policy: str = "continuous"
    ) -> Target:
        target_id = str(uuid.uuid4())
        scope = scope or [f"*.{domain}"]
        target = Target(id=target_id, domain=domain, scope=scope, scan_policy=scan_policy)
        self.targets[target_id] = target
        return target

    def get_target(self, target_id: str) -> Target | None:
        return self.targets.get(target_id)

    def get_all_targets(self) -> list[Target]:
        return list(self.targets.values())


target_manager = TargetManager()
