from sqlalchemy.exc import SQLAlchemyError

from app.models.services import Services
from app.models.users import Users
from app.schemas.logs_schema import LogCreate
from app.schemas.service_schema import ServiceCreate, ServiceOut
from app.services.auth_service import db_session
from app.services.logs_service import create_log_entry
from app.utils.pubsub import publish_ws_event


def create_service_entry(service_data: ServiceCreate, user: Users) -> Services:
    try:
        with db_session() as db:
            with db.begin():
                new_service = Services(
                    service_name=service_data.service_name,
                    status_code=service_data.status_code,
                    domain=service_data.domain,
                    org_id=user.org_id,
                )
                db.add(new_service)
                db.flush()  # get new_service.id without committing

                # Create log within same transaction
                create_log_entry(
                    db,
                    user,
                    LogCreate(
                        service_id=new_service.id,
                        status_code=service_data.status_code,
                        details={"action": "create", "domain": service_data.domain},
                    ),
                )

            service_out = ServiceOut.from_orm(new_service)

            # At this point, transaction is committed : if no error occurs

        publish_ws_event(
            {
            "type" : "service",
            "data" :
                {
                    "action": "create",
                    "service": {
                        "id": new_service.id,
                        "org_id": user.org_id,
                        "service_name": new_service.service_name,
                        "status_code": new_service.status_code,
                        "domain": new_service.domain,
                    },
                }
            }, 
            user.org_id
        )

        return service_out

    except SQLAlchemyError as e:
        raise RuntimeError(f"Service creation failed: {str(e)}") from e


def delete_service_entry(service_id: int, user: Users):
    try:
        with db_session() as db:
            with db.begin():
                service = (
                    db.query(Services)
                    .filter_by(id=service_id, org_id=user.org_id, is_deleted=False)
                    .first()
                )

                if not service:
                    return None

                service.is_deleted = True
                db.flush()

                create_log_entry(
                    db,
                    user,
                    LogCreate(
                        service_id=service.id,
                        status_code=service.status_code,
                        details={"action": "delete"},
                    ),
                )

                service_out = ServiceOut.from_orm(service)

                event_data = {
                    "id": service.id,
                    "status_code": service.status_code,
                    "domain": service.domain,
                }

        publish_ws_event(
            {
                "type" : "service",
                "data" : {"action": "delete", "service": event_data}
            },
            user.org_id
        )

        return service_out

    except SQLAlchemyError as e:
        raise RuntimeError(f"Service deletion failed: {str(e)}") from e


def update_service_status_entry(service_id: int, new_status_code: int, user: Users):
    try:
        with db_session() as db:
            with db.begin():
                service = (
                    db.query(Services)
                    .filter_by(id=service_id, org_id=user.org_id, is_deleted=False)
                    .first()
                )

                if not service:
                    return None

                service.status_code = new_status_code
                db.flush()

                create_log_entry(
                    db,
                    user,
                    LogCreate(
                        service_id=service.id,
                        status_code=new_status_code,
                        details={"action": "update_status"},
                    ),
                )

                service_out = ServiceOut.from_orm(service)

                event_data = {
                    "id": str(service.id),
                    "service_name": service.service_name,
                    "status_code": service.status_code,
                    "domain": service.domain,
                    "org_id": user.org_id,
                }

        publish_ws_event(
            {
                "type" : "service",
                "data" : {"action": "update", "service": event_data}
            },
            user.org_id
        )

        return service_out

    except SQLAlchemyError as e:
        raise RuntimeError(f"Service update failed: {str(e)}") from e


def get_services_by_org(org_id: int, page: int = 1, page_size: int = 20):
    with db_session() as db:
        query = db.query(Services).filter_by(org_id=org_id, is_deleted=False)
        total = query.count()
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
