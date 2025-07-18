from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.logs_schema import LogCreate, LogResponse
from app.services.logs_service import create_log_entry
from app.utils.auth_util import get_current_user
from app.database import get_db
from fastapi import APIRouter

router = APIRouter()

@router.post("/logs", response_model=LogResponse)
def create_log(log_data: LogCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_log_entry(db, user, log_data)
