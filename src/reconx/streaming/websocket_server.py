import asyncio
import logging

import websockets

from .event_dispatcher import event_dispatcher

logging.basicConfig(level=logging.INFO)


class WebSocketServer:
    async def handler(self, websocket, path):
        logging.info(f"Client connected to {path}")
        queue = asyncio.Queue()
        await event_dispatcher.subscribe(path, queue)

        try:
            while True:
                message = await queue.get()
                await websocket.send(message)
        except websockets.ConnectionClosed:
            logging.info(f"Client disconnected from {path}")
        finally:
            await event_dispatcher.unsubscribe(path, queue)

    async def start(self, host="localhost", port=8765):
        async with websockets.serve(self.handler, host, port):
            logging.info(f"WebSocket server started on ws://{host}:{port}")
            await asyncio.Future()  # Run forever


if __name__ == "__main__":
    server = WebSocketServer()
    asyncio.run(server.start())
