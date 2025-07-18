# app/controllers/incident_controller.py
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.auth_util import get_current_user
from app.schemas.incident_schema import *
from app.services import incident_service
from app.models.users import Users

def create_incident_controller(
    data: dict,
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user)
):
    try:
        return incident_service.create_incident(db, user, data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_incident_controller(incident_id: int, data: IncidentUpdate, db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    return incident_service.update_incident_status(db, incident_id, data)

def add_incident_update_controller(data: IncidentUpdateEntry, db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    return incident_service.add_update_to_incident(db, data)

def get_all_incidents_controller(
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user)
):
    try:
        return {
            "message": "Fetched all incidents successfully",
            "data": incident_service.get_incidents_by_org(db, user)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching incidents: {str(e)}")