from sqlalchemy.orm import Session

from app.models.status_master import StatusMaster


def get_all_statuses(db: Session):
    return db.query(StatusMaster).all()
