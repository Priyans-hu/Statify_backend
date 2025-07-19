from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.logs_schema import LogCreate, LogResponse
from app.services.logs_service import create_log_entry
from app.utils.auth_util import get_current_user

router = APIRouter()


@router.post("/logs", response_model=LogResponse)
def create_log(
    log_data: LogCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return create_log_entry(db, current_user, log_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
