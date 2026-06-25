from fastapi import APIRouter
from typing import List, Tuple

class RouterRegistry:
    def __init__(self):
        # List of (router, prefix, version, tags)
        self.routers: List[Tuple[APIRouter, str, str, List[str]]] = []
        
    def register(self, router: APIRouter, prefix: str, version: str = "v1", tags: List[str] = None):
        self.routers.append((router, prefix, version, tags or []))
        
    def get_routers(self) -> List[Tuple[APIRouter, str, str, List[str]]]:
        return self.routers

registry = RouterRegistry()
