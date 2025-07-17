from fastapi import APIRouter, Depends
from app.schemas.service_schema import ServiceCreate, ServiceOut
from app.controllers import service_controller
from typing import List

router = APIRouter(prefix="/services", tags=["Services"])

@router.post("/", response_model=ServiceOut)
def create_service(data: ServiceCreate):
    return service_controller.create_service_controller(data)

@router.delete("/{service_id}")
def delete_service(service_id: int):
    return service_controller.delete_service_controller(service_id)

@router.put("/{service_id}/status")
def update_service_status(service_id: int, new_status_code: int):
    return service_controller.update_service_status_controller(service_id, new_status_code)

@router.get("/", response_model=List[ServiceOut])
def list_services():
    return service_controller.get_services_controller()
