import os

V1_DIR = "/home/kali/ReconX/src/apps/api_gateway/gateway/v1"

routers = [
    "auth", "projects", "targets", "assets", "scans", 
    "findings", "reports", "workflows", "intelligence", "graph"
]

template = """from fastapi import APIRouter
from apps.api_gateway.gateway.router_registry import registry

router = APIRouter()

# Register the router
registry.register(router, prefix="/{name}", version="v1", tags=["{name}"])

@{name}_router_test
@router.get("/")
async def get_{name}():
    return {{"status": "ok", "service": "{name}"}}
"""

def create_v1_routers():
    os.makedirs(V1_DIR, exist_ok=True)
    open(os.path.join(V1_DIR, "__init__.py"), "a").close()
    
    for name in routers:
        filepath = os.path.join(V1_DIR, f"{name}.py")
        if not os.path.exists(filepath):
            content = template.format(name=name)
            # minor fix for the decorator syntax
            content = content.replace(f"@{name}_router_test\n", "")
            with open(filepath, "w") as f:
                f.write(content)
                
    print("[*] Created v1 REST API routers")

if __name__ == "__main__":
    create_v1_routers()
