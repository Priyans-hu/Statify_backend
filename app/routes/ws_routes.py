from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.utils.org_id_fetch import resolve_org_slug
from app.utils.websocket_manager import ws_manager
router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    org_slug = websocket.query_params.get("org")
    if not org_slug:
        await  ws_manager.disconnect(websocket)
        return
    
    org = await resolve_org_slug(org_slug)

    
    await ws_manager.connect(websocket, org.id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
