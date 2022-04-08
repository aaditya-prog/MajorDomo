from sqlalchemy import Column, Float, Integer, String

from database import Base

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
