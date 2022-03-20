from datetime import datetime
from enum import unique

from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql.sqltypes import Date

# datetime object containing current date and time
now = datetime.now()

# dd/mm/YY H:M:S
dt_string = now.strftime("%b-%d-%Y, %H:%M:%S, %A")

from database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    item_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, unique=True, index=True)
    item_category = Column(String)
    item_price = Column(Float)
    item_quantity = Column(String)
    check_in = Column(String, default=dt_string)
