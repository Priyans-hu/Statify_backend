from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import auth_routes, logs_route, service_routes
import os


def create_app():
    # from app.routes import user  # import router
    load_dotenv()
    app = FastAPI()

    app.include_router(auth_routes.router)
    app.include_router(logs_route.router)
    app.include_router(service_routes.router)

    return app