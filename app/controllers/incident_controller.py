# app/controllers/incident_controller.py
from fastapi import HTTPException

from app.schemas.incident_schema import (
    IncidentOutFull,
    IncidentUpdate,
    IncidentUpdateEntry,
)
from app.services import incident_service


def create_incident_controller(data: dict, current_user):
    try:
        return {
            "message": "Created new incident successfully",
            "data": incident_service.create_incident(current_user, data),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_incident_controller(incident_id: int, data: IncidentUpdate, current_user):
    try:
        return {
            "message": "Updated Incident successfully",
            "data": incident_service.update_incident_status(incident_id, data),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def add_incident_update_controller(data: IncidentUpdateEntry, current_user):
    try:
        return {
            "message": "Added incident update successfully",
            "data": incident_service.add_update_to_incident(data),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_all_incidents_controller(org_id):
    try:
        return {
            "message": "Fetched all incidents successfully",
            "incidents": incident_service.get_incidents_by_org(org_id),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching incidents: {str(e)}",
        )


def get_active_incidents_controller(org_id: int) -> list[IncidentOutFull]:
    return incident_service.get_active_incidents(org_id)
