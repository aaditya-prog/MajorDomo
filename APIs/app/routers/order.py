from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth.permissions import (
    ensure_cashier_or_kitchen_staff,
    ensure_is_kitchen_staff
)
from ..config import database
from ..crud import order as order_crud
from ..schemas.order import Order, OrderCreate, OrderUpdate


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
    dependencies=[Depends(ensure_cashier_or_kitchen_staff)]
)
def view_all_orders(
    status: Optional[str] = None,
    offset: Optional[int] = 0,
    limit: Optional[int] = 20,
    db: Session = Depends(get_db)
):
    return order_crud.get_orders(db, offset, limit, status)


@router.patch(
    "/{order_id}/{status_}",
    dependencies=[Depends(ensure_is_kitchen_staff)]
)
def update_order_status_by_staff(
    order_id: int, status_: str, db: Session = Depends(get_db)
):
    return order_crud.update_order_status(db, order_id, status_)
