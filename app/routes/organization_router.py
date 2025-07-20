from fastapi import APIRouter

from app.controllers.organization_controller import get_all_organizations_controller
from app.schemas.organization_schema import OrganizationOut

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/", response_model=list[OrganizationOut])
def get_all_organizations():
    return get_all_organizations_controller()
