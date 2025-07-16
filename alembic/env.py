from logging.config import fileConfig
import os
from alembic import context
from sqlalchemy import pool
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# --- Load your app's database setup and models
from app.database import engine, Base
from app.models import *  # ✅ import all models to register with metadata

# This Alembic Config object gives access to .ini values
config = context.config

# ✅ Override sqlalchemy.url from .env (ignore alembic.ini hardcoded value)
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Set up logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Use your actual metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Optional: detect type changes
        )

        with context.begin_transaction():
            context.run_migrations()


# Run correct mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
