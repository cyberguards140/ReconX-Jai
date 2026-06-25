import json

active_connections = []

def setup_websocket(sock):
    @sock.route('/ws')
    def ws(ws_conn):
        active_connections.append(ws_conn)
        ws_conn.send(json.dumps({"type": "connected", "message": "WebSocket Connected to ReconX Backend."}))
        try:
            while True:
                data = ws_conn.receive()
                if not data: break
        finally:
            active_connections.remove(ws_conn)

def broadcast(message_dict):
    msg = json.dumps(message_dict)
    for conn in list(active_connections):
        try:
            conn.send(msg)
        except Exception:
            if conn in active_connections:
                active_connections.remove(conn)
