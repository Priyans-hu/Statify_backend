from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(os.getenv('FLASK_CONFIG', 'app.config.DevelopmentConfig'))

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    with app.app_context():
    
        from app import models

        # from app.routes import register_routes
        # register_routes(app)

    return app