from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import auth_routes
import os


def create_app():
    # from app.routes import user  # import router
    load_dotenv()
    app = FastAPI()

    app.include_router(auth_routes.router)

    return app