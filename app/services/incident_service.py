# app/services/incident_service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Incidents, IncidentServiceAssociation, IncidentUpdates
from app.models.users import Users
from app.schemas.incident_schema import IncidentCreate, IncidentUpdate, IncidentUpdateEntry
from datetime import datetime

from app.services.auth_service import db_session


def create_incident(db: Session, org_id: int, data: IncidentCreate):
    if not org_id:
        raise HTTPException(status_code=400, detail="Organization ID is required")
    incident = Incidents(
        title=data.title,
        org_id=org_id,
        status=data.status,
        is_scheduled=data.is_scheduled,
        started_at=data.started_at or datetime.utcnow(),
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    for sid in data.service_ids:
        assoc = IncidentServiceAssociation(incident_id=incident.id, service_id=sid)
        db.add(assoc)

    db.commit()
    return incident


def update_incident_status(db: Session, incident_id: int, data: IncidentUpdate):
    incident = db.query(Incidents).filter_by(id=incident_id).first()

    if not incident:
        return None
    incident.status = data.status

    if data.resolved_at:
        incident.resolved_at = data.resolved_at

    db.commit()
    return incident


def add_update_to_incident(db: Session, data: IncidentUpdateEntry):
    update = IncidentUpdates(
        incident_id=data.incident_id,
        description=data.description,
        timestamp=datetime.now(),
    )
    db.add(update)

    db.commit()
    return update


def get_incidents_by_org(user):
    if not user.org_id:
        raise HTTPException(status_code=400, detail="Organization ID is required")
    with db_session() as db:
        result = db.query(Incidents).filter_by(org_id=user.org_id).all()
        print(result)
        return result if result else {"message": "No incidents found for this organization."}
