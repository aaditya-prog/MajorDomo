from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.permissions import (
    ensure_waiter_or_cashier_or_kitchen_staff,
    ensure_is_kitchen_staff,
)
from app.crud import order as order_crud
from app.dependencies.session import get_db
from app.schemas.order import Order, OrderCreate, OrderUpdate, Status

router = APIRouter(prefix="/orders", tags=["Order"])


# Add new order
@router.post("/", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return order_crud.create_order(db=db, order=order)


@router.patch("/{order_id}", response_model=Order)
def edit_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    return order_crud.update_order(db=db, order_id=order_id, order=order_update)


@router.delete("/")
def cancel_order(order_id, db: Session = Depends(get_db)):
    return order_crud.cancel_order(db=db, order_id=order_id)


@router.get(
    "/",
    response_model=list[Order],
    dependencies=[Depends(ensure_waiter_or_cashier_or_kitchen_staff)],
)
def view_all_orders(
    order_status: Optional[Status] = None,
    offset: Optional[int] = 0,
    limit: Optional[int] = 1000,
    db: Session = Depends(get_db),
):
    return order_crud.get_orders(db, offset, limit, order_status)


@router.patch(
    "/{order_id}/{order_status}", dependencies=[Depends(ensure_is_kitchen_staff)]
)
def update_order_status_by_staff(
    order_id: int, order_status: Status, db: Session = Depends(get_db)
):
    return order_crud.update_order_status(db, order_id, order_status)
