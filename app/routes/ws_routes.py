from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.utils.websocket_manager import ws_manager

router = APIRouter()


@router.websocket("/ws/services")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
