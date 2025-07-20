import datetime
import os

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Organizations
from app.models.users import Users

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

security = HTTPBearer()


def encode_auth_token(user: Users) -> str:
    try:
        payload = {
            "user_id": str(user.id),
            "role": str(user.role),
            "org_id": str(user.org_id),
            "org_slug": get_db(Organizations)
            .filter(Organizations.id == user.org_id)
            .first()
            .slug,
            "username": str(user.username),
            "exp": datetime.datetime.now() + datetime.timedelta(days=1),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    except Exception as e:
        return ""


def decode_auth_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Token expired. Please log in again."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401, detail="Invalid token. Please log in again."
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Users:
    token = credentials.credentials
    user_id = decode_auth_token(token)
    user = db.query(Users).get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    return user
