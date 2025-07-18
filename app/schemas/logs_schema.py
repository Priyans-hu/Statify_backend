from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class LogCreate(BaseModel):
    service_id: int
    status_code: int
    details: Optional[Dict] = None

class LogResponse(BaseModel):
    id: int
    org_id: int
    service_id: int
    timestamp: datetime
    status_code: int
    details: Optional[Dict]

    class Config:
        orm_mode = True