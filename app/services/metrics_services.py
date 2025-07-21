from datetime import datetime, timedelta, timezone

from sqlalchemy import or_

from app.models.incident_service_association import IncidentServiceAssociation
from app.models.incidents import Incidents
from app.models.services import Services
from app.services.auth_service import db_session


def compute_perservice_uptime(org_id):
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=90)

    with db_session() as db:
        services = db.query(Services).filter(Services.org_id == org_id).all()
        results = []

        for svc in services:
            uptime = compute_uptime(svc.id, start, end)
            results.append(
                {
                    "id": svc.id,
                    "service_name": svc.service_name,
                    "uptime": uptime,
                    "status": "Operational" if uptime > 99.8 else "Degraded",
                }
            )

    return results


def compute_uptime(service_id: int, start: datetime, end: datetime) -> float:
    with db_session() as db:
        total_duration = (end - start).total_seconds()

        incidents = (
            db.query(Incidents)
            .join(
                IncidentServiceAssociation,
                IncidentServiceAssociation.incident_id == Incidents.id,
            )
            .filter(
                IncidentServiceAssociation.service_id == service_id,
                Incidents.started_at < end,
                or_(
                    Incidents.resolved_at == None,
                    Incidents.resolved_at > start,
                ),
                Incidents.status.in_(["identified", "monitoring", "resolved"]),
            )
            .all()
        )

    downtime = 0.0
    for incident in incidents:
        incident_start = max(incident.started_at, start)
        incident_end = min(incident.resolved_at or end, end)
        downtime += (incident_end - incident_start).total_seconds()

    uptime_percent = ((total_duration - downtime) / total_duration) * 100
    return round(uptime_percent, 5)


def compute_overall_uptime(org_id: int) -> float:
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=90)

    with db_session() as db:
        services = db.query(Services).filter(Services.org_id == org_id).all()

    if not services:
        return 0.0

    total_uptime = 0.0
    for svc in services:
        uptime = compute_uptime(svc.id, start, end)
        total_uptime += uptime

    overall = total_uptime / len(services)
    return round(overall, 3)
