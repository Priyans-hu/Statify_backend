from fastapi import APIRouter, Depends

from app.controllers import incident_controller
from app.models.users import Users
from app.schemas.incident_schema import *
from app.utils.auth_util import get_current_user

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.post("/")
def create_incident(data: IncidentCreate):
    return incident_controller.create_incident_controller(data)


@router.patch("/{incident_id}")
def update_incident(incident_id: int, data: IncidentUpdate):
    return incident_controller.update_incident_controller(incident_id, data)


@router.post("/updates/")
def add_incident_update(data: IncidentUpdateEntry):
    return incident_controller.add_incident_update_controller(data)


@router.get("/")
def get_incidents(current_user: Users = Depends(get_current_user)):
    return incident_controller.get_all_incidents_controller(current_user)
