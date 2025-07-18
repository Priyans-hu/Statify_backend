from fastapi import APIRouter, HTTPException
from app.schemas.service_schema import ServiceCreate, ServiceStatusUpdate
from app.services import service_service

router = APIRouter(prefix="/services", tags=["Services"])


def create_service_controller(
    service_data: ServiceCreate,
    current_user,
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create services")
    return service_service.create_service_entry(service_data, current_user)


def delete_service_controller(
    service_id: int,
    current_user,
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete services")
    deleted = service_service.delete_service_entry(service_id, current_user)
    if not deleted:
        raise HTTPException(status_code=404, detail="Service not found or not allowed")
    return {"message": "Service deleted successfully"}


def update_service_status_controller(
    service_id: int,
    status_update: ServiceStatusUpdate,
    current_user,
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Only admins can update service status"
        )
    updated = service_service.update_service_status_entry(
        service_id, status_update.status_code, current_user
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Service not found or not allowed")
    return updated


def get_services_controller(
    current_user
):
    return service_service.get_services_by_org(current_user.org_id)
