from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import status_controller
from app.database import get_db
from app.schemas.status_schema import StatusOut

router = APIRouter(prefix="/status", tags=["Status"])


# status_routes.py
@router.get("/", response_model=List[StatusOut])
def list_all_statuses(db: Session = Depends(get_db)):
    return status_controller.fetch_statuses(db)
