from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import asyncio
from apps.api_gateway.gateway.router_registry import registry
from recon.services.pipeline_engine import pipeline_engine
from core.messaging.broker import broker

router = APIRouter()
registry.register(router, prefix="/ws", version="v1", tags=["websocket"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.consumer_started = False
        broker.subscribe("ws_broadcast", self.handle_broker_message)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        if not self.consumer_started:
            self.consumer_started = True
            asyncio.create_task(broker.start_consumer("ws_broadcast"))
        await self.broadcast({"type": "info", "message": "Backend WebSocket connected successfully."})

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections.copy():
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                self.active_connections.remove(connection)
                
    async def handle_broker_message(self, payload: dict):
        await self.broadcast(payload)

manager = ConnectionManager()

@router.websocket("/live")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                if msg.get("action") == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket)
