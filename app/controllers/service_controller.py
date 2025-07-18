from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.service_schema import ServiceCreate, ServiceStatusUpdate, ServiceOut
from app.services import service_service
from app.utils.auth_util import get_current_user
from app.database import get_db
from app.models.users import Users

router = APIRouter(prefix="/services", tags=["Services"])

def create_service_controller(
    service_data: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create services")
    return service_service.create_service_entry(service_data, current_user, db)

def delete_service_controller(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete services")
    deleted = service_service.delete_service_entry(service_id, current_user, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Service not found or not allowed")
    return {"message": "Service deleted successfully"}


def update_service_status_controller(
    service_id: int,
    status_update: ServiceStatusUpdate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update service status")
    updated = service_service.update_service_status_entry(service_id, status_update.status_code, current_user, db)
    if not updated:
        raise HTTPException(status_code=404, detail="Service not found or not allowed")
    return updated


def get_services_controller(
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return service_service.get_services_by_org(current_user.org_id, db)
