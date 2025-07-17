from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.service_schema import ServiceCreate
from app.services import service_service
from app.utils.auth_util import get_current_user
from app.database import get_db
from app.models.users import Users


def create_service_controller(data: ServiceCreate, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create services")
    return service_service.create_service(db, current_user.org_id, data)

def delete_service_controller(service_id: int, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete services")
    deleted = service_service.delete_service(db, service_id, current_user.org_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Service not found or not allowed")
    return {"message": "Service deleted successfully"}

def update_service_status_controller(service_id: int, new_status_code: int, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update service status")
    updated = service_service.update_service_status(db, service_id, current_user.org_id, new_status_code)
    if not updated:
        raise HTTPException(status_code=404, detail="Service not found or not allowed")
    return updated

def get_services_controller(db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
    return service_service.get_services_by_org(db, current_user.org_id)
