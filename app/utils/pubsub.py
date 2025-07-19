import asyncio
import logging

from app.utils.websocket_manager import ws_manager

logger = logging.getLogger(__name__)


def publish_ws_event(event: dict):
    try:
        asyncio.create_task(_safe_broadcast(event))
    except Exception as e:
        logger.warning(f"Failed to schedule WebSocket broadcast: {e}")


async def _safe_broadcast(event: dict):
    try:
        await ws_manager.broadcast(event)
    except Exception as e:
        logger.warning(f"WebSocket broadcast failed: {e}")
