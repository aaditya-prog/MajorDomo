from sqlalchemy import (Column, Float, Integer,
                        String, func)


from ..config.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    item_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, unique=True, index=True)
    item_category = Column(String)
    item_price = Column(Float)
    item_quantity = Column(String)
    check_in = Column(String, server_default=func.now())
