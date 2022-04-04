from sqlalchemy import DECIMAL, Column, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Date, JSON
from database import Base

"""
    Model: users
    Description: Stores the attributes of the users that will interact with the APIs.

"""


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String, index=True)
    password = Column(String)
    staff_type = Column(String)


"""
    Model: Menu
    Description: Stores the attributes of the food items stored in the menu.

"""


class Food(Base):
    __tablename__ = "menu"

    food_id = Column(Integer, primary_key=True, index=True)
    food_name = Column(String, unique=True, index=True)
    food_category = Column(String)
    food_price = Column(Float)


class Orders(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    items = Column(JSON, nullable=False)
    order_date = Column(Date, server_default=func.now())
    table = Column(Integer, nullable=False)

