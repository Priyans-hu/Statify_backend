from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
import os

def create_app():
    from fastapi import FastAPI
    from dotenv import load_dotenv

    # Load environment variables from .env file
    load_dotenv()

    app = FastAPI()
    # Database configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db") 
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base = declarative_base()



    # Include your routes, middleware, and other configurations here
    # For example:
    # from app.routes import router
    # app.include_router(router)

    return app