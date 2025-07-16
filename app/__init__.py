from fastapi import FastAPI
from dotenv import load_dotenv
import os


def create_app():
    from app.routes import user  # import router
    load_dotenv()
    app = FastAPI()
    
    app.include_router(user.router)

    return app