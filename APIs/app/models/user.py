from sqlalchemy import Column, Integer, String

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
    staff = Column(String)
