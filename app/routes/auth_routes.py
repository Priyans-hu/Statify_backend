from fastapi import APIRouter, Depends
from app.controllers.auth_controller import register_user, login_user, logout_user
from app.utils.auth_util import get_current_user
from app.models.users import Users

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(data: dict):
    return register_user(data)

@router.post("/login")
def login(data: dict):
    return login_user(data)

@router.post("/logout")
def logout(current_user: Users = Depends(get_current_user)):
    return logout_user(current_user)
