from fastapi import APIRouter
from app.controllers import logs_controller

router = APIRouter()

router.include_router(logs_controller.router, tags=["Logs"])