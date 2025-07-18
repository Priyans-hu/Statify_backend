from typing import Optional

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    password: str
    org_id: int


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
