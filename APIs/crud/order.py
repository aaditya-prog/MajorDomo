from sqlalchemy.orm import Session

from models.order import Orders
from schemas.order import OrderCreate


# Create Order
def create_order(db: Session, order: OrderCreate):
    db_order = Orders(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
