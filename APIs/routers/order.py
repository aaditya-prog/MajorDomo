from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud import order as order_crud
from schemas.order import Order, OrderCreate

import database

router = APIRouter(prefix="/orders")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Add new order
@router.post("/order/create/", response_model=Order, tags=["Order"])
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return order_crud.create_order(db=db, order=order)
