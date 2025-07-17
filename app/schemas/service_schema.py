from pydantic import BaseModel, Field
from typing import Optional

class ServiceCreate(BaseModel):
    service_name: str
    status_code: int
    domain: Optional[str] = None

class ServiceOut(BaseModel):
    id: int
    service_name: str
    org_id: int
    status_code: int
    domain: Optional[str] = None

    class Config:
        orm_mode = True