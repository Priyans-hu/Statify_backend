from fastapi import HTTPException, status

from app.services.auth_service import login_user_service, register_user_service


def register_user(data: dict):
    try:
        result = register_user_service(data)
        return {"message": "User registered successfully.", "data": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}",
        )


def login_user(data: dict, org_id: int):
    try:
        result = login_user_service(data, org_id)
        return {"message": "Login successful.", "data": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Login failed: {str(e)}"
        )


def logout_user(user):
    try:
        return {"message": f"User {user.username} logged out successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}",
        )


def current_user_controller(current_user):
    try:
        return {"Logged In User": {current_user}}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Failed to retrieve current user: {str(e)}",
        )
