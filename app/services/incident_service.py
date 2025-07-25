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
from app.utils.pubsub import publish_ws_event
from app.utils.serialize_datetimes import serialize_datetime


def create_incident(current_user, data: IncidentCreate):
    if not current_user.org_id:
        raise HTTPException(status_code=400, detail="Organization ID is required")
    try:
        incident = Incidents(
            title=data.title,
            org_id=current_user.org_id,
            description=data.description,
            status=data.status,
            is_scheduled=data.is_scheduled,
            started_at=data.started_at or datetime.now(),
        )
        with db_session() as db:
            db.add(incident)
            db.commit()
            db.refresh(incident)

            for sid in data.service_ids:
                assoc = IncidentServiceAssociation(
                    incident_id=incident.id, service_id=sid
                )
                db.add(assoc)

            db.commit()

            incident_out = get_incident_by_id(incident.id)
            incident_out = serialize_datetime(incident_out)

        publish_ws_event(
            {
                "type": "incident",
                "data": {"action": "create", "incident": incident_out},
            },
            current_user.org_id,
        )

        return incident_out
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create incident: {str(e)}"
        )


def update_incident_status(incident_id: int, data: IncidentUpdate, user):
    if not user.org_id:
        raise HTTPException(status_code=400, detail="Organization ID is required")
    try:
        with db_session() as db:
            incident = db.query(Incidents).filter_by(id=incident_id).first()

            if not incident:
                return None

            incident.status = data.status

            if data.description is not None:
                add_update_to_incident(
                    IncidentUpdateEntry(
                        **{"incident_id": incident_id, "description": data.description}
                    ),
                    user,
                )

            if data.resolved_at:
                incident.resolved_at = data.resolved_at

            db.commit()

            db.refresh(incident)

        incident_out = get_incident_by_id(incident_id)
        incident_out = serialize_datetime(incident_out)

        publish_ws_event(
            {
                "type": "incident",
                "data": {"action": "update", "incident": incident_out},
            },
            user.org_id,
        )

        return incident

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update incident: {str(e)}"
        )


def add_update_to_incident(data: IncidentUpdateEntry, user):
    if not user.org_id:
        raise HTTPException(status_code=400, detail="Organization ID is required")
    with db_session() as db:
        update = IncidentUpdates(
            incident_id=data.incident_id,
            description=data.description,
            created_at=datetime.now(),
        )
        db.add(update)

        db.commit()

    incident_out = get_incident_by_id(data.incident_id)
    incident_out = serialize_datetime(incident_out)

    publish_ws_event(
        {
            "type": "incident",
            "data": {"action": "add_update", "incident": incident_out},
        },
        user.org_id,
    )

    return update


def get_incidents_by_org(org_id: int):
    if not org_id:
        raise HTTPException(status_code=400, detail="Organization ID is required")
    with db_session() as db:
        incidents = db.query(Incidents).filter_by(org_id=org_id).all()

        if not incidents:
            return []

        result = []
        for incident in incidents:
            incident_data = get_incident_by_id(incident.id)
            incident_data = serialize_datetime(incident_data)
            if incident_data:
                result.append(incident_data)

        return result


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
            incident_data = serialize_datetime(incident_data)
            if incident_data:
                result.append(incident_data)

        return result


def get_incident_by_id(incident_id: int):
    with db_session() as db:
        incident = db.query(Incidents).filter_by(id=incident_id).first()

        if not incident:
            return None

        affected_services = (
            db.query(Services)
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
                    "service_name": s.service_name,
                    "org_id": s.org_id,
                    "status_code": s.status_code,
                    "domain": s.domain,
                }
                for s in affected_services
            ],
            "updates": [
                {
                    "id": update.id,
                    "description": update.description,  # 'message' maps to 'description'
                    "timestamp": update.created_at,  # 'created_at' maps to 'timestamp'
                }
                for update in incident_updates
            ],
        }
