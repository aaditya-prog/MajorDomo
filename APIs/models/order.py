from sqlalchemy import Column, Date, func, JSON, Integer

from database import Base


class Orders(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    items = Column(JSON, nullable=False)
    order_date = Column(Date, server_default=func.now())
    table = Column(Integer, nullable=False)
