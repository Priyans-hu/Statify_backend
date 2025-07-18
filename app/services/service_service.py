from sqlalchemy.orm import Session

from app.models.services import Services
from app.models.users import Users
from app.schemas.service_schema import ServiceCreate
from app.schemas.logs_schema import LogCreate
from app.services.logs_service import create_log_entry


def create_service_entry(
    service_data: ServiceCreate,
    user: Users,
    db: Session
) -> Services:
    new_service = Services(
        service_name=service_data.service_name,
        status_code=service_data.status_code,
        domain=service_data.domain,
        org_id=user.org_id
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    create_log_entry(db, user, LogCreate(
        service_id=new_service.id,
        status_code=service_data.status_code,
        details={"action": "create", "domain": service_data.domain}
    ))

    return new_service


def delete_service_entry(
    service_id: int,
    user: Users,
    db: Session
):
    service = db.query(Services).filter_by(
        id=service_id,
        org_id=user.org_id,
        is_deleted=False
    ).first()

    if service:
        service.is_deleted = True
        db.commit()

        create_log_entry(db, user, LogCreate(
            service_id=service.id,
            status_code=service.status_code,
            details={"action": "delete"}
        ))

        return service
    return None


def update_service_status_entry(
    service_id: int,
    new_status_code: int,
    user: Users,
    db: Session
):
    service = db.query(Services).filter_by(
        id=service_id,
        org_id=user.org_id,
        is_deleted=False
    ).first()

    if service:
        service.status_code = new_status_code
        db.commit()

        create_log_entry(db, user, LogCreate(
            service_id=service.id,
            status_code=new_status_code,
            details={"action": "update_status"}
        ))

        return service
    return None


def get_services_by_org(
    org_id: int,
    db: Session
):
    return db.query(Services).filter_by(
        org_id=org_id,
        is_deleted=False
    ).all()
