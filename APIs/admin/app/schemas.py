from datetime import datetime, date
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    username: str
    full_name: str


class Staff(str, Enum):
    INVENTORY_STAFF = "Inventory Staff"
    KITCHEN_STAFF = "Kitchen Staff"
    CASHIER = "Cashier"
    ADMIN = "Admin"


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


"""
    Food menu schema

"""


class FoodData(BaseModel):
    food_name: str
    food_category: str
    food_price: float


class Food(FoodData):
    food_id: int

    class Config:
        orm_mode = True


"""
    Order schema

"""


class OrderBase(BaseModel):
    items: list[int]
    table: int

    @validator('table')
    def table_is_valid(cls, v):
        if v < 1 or v > 8:
            raise ValueError('Not a valid table number')
        return v


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    order_id: int
    order_date: date

