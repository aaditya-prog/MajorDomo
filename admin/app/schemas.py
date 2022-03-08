from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    full_name: str


class Staff(str, Enum):
    INVENTORY_STAFF = "Inventory Staff"
    KITCHEN_STAFF = "Kitchen Staff"
    CASHIER = "Cashier"


class UserCreate(UserBase):
    password: str
    staff: Staff


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str
