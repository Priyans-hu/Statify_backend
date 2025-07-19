from sqlalchemy.orm import Session

from app.services.status_service import get_all_statuses


def fetch_statuses(db: Session):
    return get_all_statuses(db)
