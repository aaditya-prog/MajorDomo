from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.permissions import ensure_can_view_order
from crud import order as order_crud
from schemas.order import Order, OrderCreate, OrderUpdate

import database

router = APIRouter(prefix="/orders", tags=["Order"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Add new order
@router.post("/", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return order_crud.create_order(db=db, order=order)


@router.patch("/{order_id}", response_model=Order)
def edit_order(
    order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)
):
    return order_crud.update_order(
        db=db, order_id=order_id, order=order_update
    )


@router.delete("/")
def cancel_order(order_id, db: Session = Depends(get_db)):
    return order_crud.cancel_order(db=db, order_id=order_id)


@router.get(
    "/",
    response_model=list[Order],
    dependencies=[Depends(ensure_can_view_order)]
)
def view_all_orders(
    offset: int = 0, limit: int = 20, db: Session = Depends(get_db)
):
    return order_crud.get_orders(db, offset, limit)
