from pydantic import BaseModel


class StatusOut(BaseModel):
    id: int
    status: str

    class Config:
        from_attributes = True
