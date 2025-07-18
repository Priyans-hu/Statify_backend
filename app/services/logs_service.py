from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.logs import Logs
from app.models.services import Services
from app.models.users import Users
from app.schemas.logs_schema import LogCreate


def create_log_entry(db: Session, user: Users, log_data: LogCreate):
    service = db.query(Services).filter(Services.id == log_data.service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    log = Logs(
        org_id=user.org_id,
        service_id=log_data.service_id,
        status_code=log_data.status_code,
        details=log_data.details,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
