import os

from functools import lru_cache
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, EmailStr

# Utilizing dotenv to load environment variables from the OS.
env_path = Path(".env")
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # Project Details
    PROJECT_NAME: Optional[str] = "FastAPI Restaurant Management System(RMS)"
    PROJECT_VERSION: Optional[str] = "1.0.0"

    # Database Configuration Settings
    POSTGRES_USER: Optional[str] = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: Optional[str] = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: Optional[str] = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: Optional[str] = os.getenv("POSTGRES_DB")
    DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


# Using the @lru_cache() decorator on top,
# the Settings object will be created only once, the first time it's called.
@lru_cache()
def get_settings():
    return Settings()
