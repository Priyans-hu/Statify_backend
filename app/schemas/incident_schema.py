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
    incident_id: int
    status: str
    description: Optional[str] = None
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


class ServiceOut(BaseModel):
    id: int
    service_name: str
    domain: str

    class Config:
        orm_mode = True


class IncidentUpdateOut(BaseModel):
    id: int
    description: str
    timestamp: datetime

    class Config:
        orm_mode = True


class IncidentOutFull(BaseModel):
    id: int
    title: str
    description: Optional[str]
    org_id: int
    status: str
    is_scheduled: bool
    started_at: datetime
    resolved_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    services: list[ServiceOut]
    updates: list[IncidentUpdateOut]

    class Config:
        orm_mode = True
