from fastapi import HTTPException

from app.services.metrics_services import (
    compute_overall_uptime,
    compute_perservice_uptime,
)


def get_service_uptime_metrics_controller(org_id: int):
    try:
        return compute_perservice_uptime(org_id)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error computing service uptime: {str(e)}"
        )


def get_overall_uptime_metric_controller(org_id: int):
    try:
        return {"overall_uptime_90d": compute_overall_uptime(org_id)}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error computing overall uptime: {str(e)}"
        )


def get_complete_mtreric_controller(org_id: int):
    try:
        return {
            "overall_uptime_90d": compute_overall_uptime(org_id),
            "services_uptime": compute_perservice_uptime(org_id),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error computing overall uptime: {str(e)}"
        )
