from app.services.auth_service import register_user_service, login_user_service

def register_user(data: dict):
    return register_user_service(data)

def login_user(data: dict):
    return login_user_service(data)

def logout_user(user):
    return {"message": f"User {user.username} logged out successfully."}
