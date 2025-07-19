from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel


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
        from_attributes = True
