from app.core.event_loop import get_event_loop
import asyncio
import logging
from app.utils.websocket_manager import ws_manager

logger = logging.getLogger(__name__)

def publish_ws_event(event: dict, org_id: int = None):
    try:
        loop = get_event_loop()
        if loop is None:
            raise RuntimeError("Event loop not initialized")
        if org_id is not None:
            print(org_id)
            asyncio.run_coroutine_threadsafe(_safe_broadcast(event, org_id), loop)
    except Exception as e:
        logger.warning(f"Failed to schedule WebSocket broadcast: {e}")

async def _safe_broadcast(event: dict, org_id:int):
    try:
        await ws_manager.broadcast(event, org_id)
    except Exception as e:
        logger.warning(f"WebSocket broadcast failed: {e}")
