from sqlalchemy.exc import SQLAlchemyError

from app.models.services import Services
from app.models.users import Users
from app.schemas.logs_schema import LogCreate
from app.schemas.service_schema import ServiceCreate
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
                    user,
                    LogCreate(
                        service_id=new_service.id,
                        status_code=service_data.status_code,
                        details={"action": "create", "domain": service_data.domain},
                    ),
                )

            # At this point, transaction is committed

        publish_ws_event(
            {
                "action": "create",
                "service": {
                    "id": new_service.id,
                    "name": new_service.service_name,
                    "status_code": new_service.status_code,
                    "domain": new_service.domain,
                },
            }
        )

        return new_service

    except SQLAlchemyError as e:
        raise RuntimeError(f"Service creation failed: {str(e)}") from e


def delete_service_entry(service_id: int, user: Users):
    with db_session() as db:
        service = (
            db.query(Services)
            .filter_by(id=service_id, org_id=user.org_id, is_deleted=False)
            .first()
        )

        if service:
            service.is_deleted = True
            db.commit()

            create_log_entry(
                user,
                LogCreate(
                    service_id=service.id,
                    status_code=service.status_code,
                    details={"action": "delete"},
                ),
            )

            publish_ws_event(
                {
                    "action": "delete",
                    "service": {
                        "id": service.id,
                        "status_code": service.status_code,
                        "domain": service.domain,
                    },
                }
            )

            return service
    return None


def update_service_status_entry(service_id: int, new_status_code: int, user: Users):
    with db_session() as db:
        service = (
            db.query(Services)
            .filter_by(id=service_id, org_id=user.org_id, is_deleted=False)
            .first()
        )

        if service:
            service.status_code = new_status_code
            db.commit()

            create_log_entry(
                user,
                LogCreate(
                    service_id=service.id,
                    status_code=new_status_code,
                    details={"action": "update_status"},
                ),
            )

            publish_ws_event(
                {
                    "action": "create",
                    "service": {
                        "id": service.id,
                        "name": service.service_name,
                        "status_code": service.status_code,
                        "domain": service.domain,
                    },
                }
            )

            return service
    return None


def get_services_by_org(org_id: int):
    with db_session() as db:
        return db.query(Services).filter_by(org_id=org_id, is_deleted=False).all()
