from fastapi import APIRouter


class RouterRegistry:
    def __init__(self):
        # List of (router, prefix, version, tags)
        self.routers: list[tuple[APIRouter, str, str, list[str]]] = []

    def register(self, router: APIRouter, prefix: str, version: str = "v1", tags: list[str] = None):
        self.routers.append((router, prefix, version, tags or []))

    def get_routers(self) -> list[tuple[APIRouter, str, str, list[str]]]:
        return self.routers


registry = RouterRegistry()
