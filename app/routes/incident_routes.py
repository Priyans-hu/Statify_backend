from fastapi import APIRouter, Depends, Request

from app.controllers import incident_controller
from app.models.users import Users
from app.schemas.incident_schema import *
from app.utils.auth_util import get_current_user

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.post("/")
def create_incident(data: IncidentCreate, current_user: Users = Depends(get_current_user)):
    return incident_controller.create_incident_controller(data, current_user)


@router.patch("/{incident_id}")
def update_incident(incident_id: int, data: IncidentUpdate, current_user: Users = Depends(get_current_user)):
    return incident_controller.update_incident_controller(incident_id, data, current_user)


@router.post("/updates/")
def add_incident_update(data: IncidentUpdateEntry, current_user: Users = Depends(get_current_user)):
    return incident_controller.add_incident_update_controller(data, current_user)


@router.get("/")
def get_incidents(request: Request):
    org_id = request.state.org_id
    return incident_controller.get_all_incidents_controller(org_id)
