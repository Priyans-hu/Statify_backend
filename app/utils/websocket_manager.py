from typing import Dict, List

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, org_id: int):
        await websocket.accept()
        if org_id not in self.active_connections:
            self.active_connections[org_id] = []
        self.active_connections[org_id].append(websocket)

    def disconnect(self, websocket: WebSocket):
        for org_id, connections in self.active_connections.items():
            if websocket in connections:
                connections.remove(websocket)
                # Optional cleanup if empty
                if not connections:
                    del self.active_connections[org_id]
                break

    async def broadcast(self, message: dict, org_id: int):
        if org_id is not None:
            connections = self.active_connections.get(org_id, [])
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass

ws_manager = ConnectionManager()
