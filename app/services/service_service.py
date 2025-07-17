from sqlalchemy.orm import Session
from app.models.services import Services
from app.schemas.service_schema import ServiceCreate

def create_service(db: Session, org_id: int, data: ServiceCreate) -> Services:
    service = Services(
        service_name=data.service_name,
        status_code=data.status_code,
        domain=data.domain,
        org_id=org_id
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

def delete_service(db: Session, service_id: int, org_id: int):
    service = db.query(Services).filter_by(id=service_id, org_id=org_id, is_deleted=False).first()
    if service:
        service.is_deleted = True
        db.commit()
        return service
    return None

def update_service_status(db: Session, service_id: int, org_id: int, new_status_code: int):
    service = db.query(Services).filter_by(id=service_id, org_id=org_id, is_deleted=False).first()
    if service:
        service.status_code = new_status_code
        db.commit()
        return service
    return None

def get_services_by_org(db: Session, org_id: int):
    return db.query(Services).filter_by(org_id=org_id, is_deleted=False).all()
