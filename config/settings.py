import os
import urllib

from functools import lru_cache
from pathlib import Path
from typing import Optional

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseSettings, EmailStr

# Utilizing dotenv to load environment variables from the OS.
env_path = find_dotenv()
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # Project Details
    PROJECT_NAME: Optional[str] = "FastAPI Restaurant Management System(RMS)"
    PROJECT_VERSION: Optional[str] = "1.0.0"
    #
    # # Database Configuration Settings
    # POSTGRES_USER: Optional[str] = os.getenv("POSTGRES_USER")
    # POSTGRES_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD")
    # POSTGRES_SERVER: Optional[str] = os.getenv("POSTGRES_SERVER", "localhost")
    # POSTGRES_PORT: Optional[str] = os.getenv("POSTGRES_PORT")
    # POSTGRES_DB: Optional[str] = os.getenv("POSTGRES_DB")
    # SSL_MODE: Optional[str] = os.getenv("SSL_MODE")
    # DATABASE_URL = (
    #     f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}?sslmode={SSL_MODE}"
    # )

    host_server = os.environ.get('host_server', 'localhost')
    db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
    database_name = os.environ.get('database_name', 'fastapi')
    db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'postgres')))
    db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'secret')))
    ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode', 'prefer')))

    DATABASE_URL = (
        f"postgresql://{db_username}:{db_password}@{db_password}:{db_server_port}/{database_name}?sslmode={ssl_mode}"
    )

# Using the @lru_cache() decorator on top,
# the Settings object will be created only once, the first time it's called.
@lru_cache()
def get_settings():
    return Settings()
