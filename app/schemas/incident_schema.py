from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class IncidentCreate(BaseModel):
    title: str
    status: str  # "investigating", "identified", "monitoring", "resolved"
    is_scheduled: bool = False
    service_ids: List[int]
    started_at: Optional[datetime] = None


class IncidentUpdate(BaseModel):
    status: str
    resolved_at: Optional[datetime] = None


class IncidentUpdateEntry(BaseModel):
    incident_id: int
    description: str


class IncidentOut(BaseModel):
    id: int
    title: str
    status: str
    is_scheduled: bool
    started_at: datetime
    resolved_at: Optional[datetime]
    service_ids: List[int]

    class Config:
        from_attributes = True
