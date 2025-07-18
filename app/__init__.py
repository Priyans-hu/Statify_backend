from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import (
    auth_routes,
    incident_routes,
    logs_route,
    service_routes,
    ws_routes,
)


def create_app():
    # from app.routes import user  # import router
    load_dotenv()
    app = FastAPI()
    # Corss Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_routes.router)
    app.include_router(logs_route.router)
    app.include_router(service_routes.router)
    app.include_router(ws_routes.router)
    app.include_router(incident_routes.router)

    return app
