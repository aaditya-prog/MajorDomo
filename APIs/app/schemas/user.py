from enum import Enum

from pydantic import BaseModel


class Staff(str, Enum):
    INVENTORY_STAFF = "Inventory Staff"
    KITCHEN_STAFF = "Kitchen Staff"
    CASHIER = "Cashier"
    ADMIN = "Admin"


class UserBase(BaseModel):
    username: str
    full_name: str
    staff: Staff


class UserCreate(UserBase):
    password: str


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
