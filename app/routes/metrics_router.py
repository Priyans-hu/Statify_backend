from fastapi import APIRouter, Request
from fastapi_cache.decorator import cache

from app.controllers.metrics_controller import (
    get_complete_mtreric_controller,
    get_overall_uptime_metric_controller,
    get_service_uptime_metrics_controller,
)

router = APIRouter(prefix="/metrics", tags=["Metrics"])


@router.get("/services")
def get_all_service_uptimes(request: Request):
    org_id = request.state.org_id
    return get_service_uptime_metrics_controller(org_id)


@router.get("/overall-uptime")
def get_overall_uptime_route(request: Request):
    org_id = request.state.org_id
    return get_overall_uptime_metric_controller(org_id)


@router.get("/")
@cache(expire=1800)  # cache for 30 minutes
def get_complete_metrics(request: Request):
    org_id = request.state.org_id
    return get_complete_mtreric_controller(org_id)
