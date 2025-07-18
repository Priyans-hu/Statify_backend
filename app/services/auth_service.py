import uuid
from contextlib import contextmanager

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.users import Users
from app.utils.auth_util import encode_auth_token
from app.utils.password import hash_password, verify_password


@contextmanager
def db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


def register_user_service(data: dict):
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    org_id = data.get("org_id")
    role = data.get("role", "viewer")

    if not password:
        raise ValueError("Password is required")

    with db_session() as db:
        existing = db.query(Users).filter_by(username=username).first()
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")

        hashedPassword = hash_password(password)
        user = Users(
            id=uuid.uuid4(),
            username=username,
            email=email,
            org_id=org_id,
            role=role,
            password_hash=hashedPassword,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message": "User registered successfully", "user_id": str(user.id)}


def login_user_service(data: dict):
    username = data.get("username")
    password = data.get("password")

    with db_session() as db:
        user = db.query(Users).filter_by(username=username).first()
        if password is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = encode_auth_token(user.id)
        return {"access_token": token, "token_type": "bearer"}
