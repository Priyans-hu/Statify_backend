from fastapi import APIRouter, Depends, Request

from app.controllers import service_controller
from app.models.users import Users
from app.schemas.service_schema import ServiceCreate, ServiceOut, ServiceStatusUpdate
from app.utils.auth_util import get_current_user

router = APIRouter(prefix="/services", tags=["Services"])


@router.post("/", response_model=ServiceOut)
def create_service(
    service_data: ServiceCreate,
    current_user: Users = Depends(get_current_user),
):
    return service_controller.create_service_controller(service_data, current_user)


@router.delete("/{service_id}", status_code=204)
def delete_service(
    service_id: int,
    current_user: Users = Depends(get_current_user),
):
    return service_controller.delete_service_controller(service_id, current_user)


@router.patch("/{service_id}/status", response_model=ServiceOut)
def update_service_status(
    service_id: int,
    status_update: ServiceStatusUpdate,
    current_user: Users = Depends(get_current_user),
):
    return service_controller.update_service_status_controller(
        service_id, status_update, current_user
    )


@router.get("/", response_model=list[ServiceOut])
def get_services(request: Request):
    org_id = request.state.org_id
    return service_controller.get_services_controller(org_id)
