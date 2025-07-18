from typing import Optional

from pydantic import BaseModel, Field


class ServiceCreate(BaseModel):
    service_name: str
    status_code: int
    domain: Optional[str] = None


class ServiceStatusUpdate(BaseModel):
    status_code: int = Field(..., description="New status code for the service")


class ServiceOut(BaseModel):
    id: int
    service_name: str
    org_id: int
    status_code: int
    domain: Optional[str] = None

    class Config:
        from_attributes = True
