# app/services/incident_service.py
from datetime import datetime

from fastapi import HTTPException

from app.models import Incidents, IncidentServiceAssociation, IncidentUpdates, Services
from app.schemas.incident_schema import (
    IncidentCreate,
    IncidentOutFull,
    IncidentUpdate,
    IncidentUpdateEntry,
)
from app.services.auth_service import db_session


def create_incident(current_user, data: IncidentCreate):
    if not current_user.org_id:
        raise HTTPException(status_code=400, detail="Organization ID is required")
    incident = Incidents(
        title=data.title,
        org_id=current_user.org_id,
        status=data.status,
        is_scheduled=data.is_scheduled,
        started_at=data.started_at or datetime.now(),
    )

    with db_session() as db:
        db.add(incident)
        db.commit()
        db.refresh(incident)

        for sid in data.service_ids:
            assoc = IncidentServiceAssociation(incident_id=incident.id, service_id=sid)
            db.add(assoc)

        db.commit()

    return incident


def update_incident_status(incident_id: int, data: IncidentUpdate):
    with db_session() as db:
        incident = db.query(Incidents).filter_by(id=incident_id).first()

        if not incident:
            return None
        incident.status = data.status

        if data.resolved_at:
            incident.resolved_at = data.resolved_at

        db.commit()
    return incident


def add_update_to_incident(data: IncidentUpdateEntry):
    with db_session() as db:
        update = IncidentUpdates(
            incident_id=data.incident_id,
            description=data.description,
            timestamp=datetime.now(),
        )
        db.add(update)

        db.commit()
    return update


def get_incidents_by_org(org_id: int):
    if not org_id:
        raise HTTPException(status_code=400, detail="Organization ID is required")
    with db_session() as db:
        result = db.query(Incidents).filter_by(org_id=org_id).all()
        return (
            result
            if result
            else {"message": "No incidents found for this organization."}
        )


def get_active_incidents(org_id: int) -> list[IncidentOutFull]:
    with db_session() as db:
        active_incidents = (
            db.query(Incidents)
            .filter(Incidents.org_id == org_id, Incidents.resolved_at.is_(None))
            .all()
        )

        if not active_incidents:
            return []

        result = []
        for incident in active_incidents:
            incident_data = get_incident_by_id(incident.id)
            if incident_data:
                result.append(incident_data)

        return result


def get_incident_by_id(incident_id: int):
    with db_session() as db:
        incident = db.query(Incidents).filter_by(id=incident_id).first()
        if not incident:
            return None

        affected_services = (
            db.query(Services.id, Services.service_name)
            .join(
                IncidentServiceAssociation,
                Services.id == IncidentServiceAssociation.service_id,
            )
            .filter(IncidentServiceAssociation.incident_id == incident_id)
            .all()
        )

        incident_updates = (
            db.query(IncidentUpdates)
            .filter_by(incident_id=incident_id)
            .order_by(IncidentUpdates.created_at)
            .all()
        )

        return {
            "id": incident.id,
            "title": incident.title,
            "description": incident.description,
            "org_id": incident.org_id,
            "status": incident.status,
            "is_scheduled": incident.is_scheduled,
            "started_at": incident.started_at,
            "resolved_at": incident.resolved_at,
            "created_at": incident.created_at,
            "updated_at": incident.updated_at,
            "services": [
                {
                    "id": s.id,
                    "service_name": s.name,
                    "org_id": s.org_id,
                    "status_code": s.status_code,
                    "domain": s.domain,
                }
                for s in affected_services
            ],
            "updates": [
                {
                    "id": update.id,
                    "description": update.message,  # 'message' maps to 'description'
                    "timestamp": update.created_at,  # 'created_at' maps to 'timestamp'
                }
                for update in incident_updates
            ],
        }
