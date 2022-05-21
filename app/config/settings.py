import os

from functools import lru_cache
from typing import Optional
from urllib.parse import quote_plus

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseSettings

# Utilizing dotenv to load environment variables from the OS.
env_path = find_dotenv()
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # Project Details
    PROJECT_NAME: Optional[str] = "FastAPI Restaurant Management System(RMS)"
    PROJECT_VERSION: Optional[str] = "1.0.0"
    #
    # Database Configuration Settings
    DATABASE_URL = "sqlite:///majordomo.db"
# Using the @lru_cache() decorator on top,
# the Settings object will be created only once, the first time it's called.
@lru_cache()
def get_settings():
    return Settings()
