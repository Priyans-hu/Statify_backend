import jwt
import os
import datetime
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.users import Users

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

security = HTTPBearer()

def encode_auth_token(user_id: str) -> str:
    try:
        payload = {
            'user_id': str(user_id),
            'exp': datetime.datetime.now() + datetime.timedelta(days=1)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    except Exception as e:
        return None

def decode_auth_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token. Please log in again.")

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Users:
    token = credentials.credentials
    user_id = decode_auth_token(token)
    user = db.query(Users).get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    return user
