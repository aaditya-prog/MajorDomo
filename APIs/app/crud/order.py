from typing import Optional, Union
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.order import Orders
from schemas.order import OrderCreate, OrderUpdate, Status


def get_existing_order(db: Session, order_id: int):
    db_order: Union[Orders, None]
    db_order = db.query(Orders).filter(Orders.order_id == order_id).first()
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No record of such order"
        )

    return db_order


def ensure_order_is_not_cancelled(db_order: Orders):
    if db_order.status == Status.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order has already been cancelled"
        )


def ensure_order_is_not_paid_for(db_order: Orders):
    if db_order.status == Status.PAID:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order has already been paid for"
        )


def ensure_order_is_not_already_prepared(db_order: Orders):
    if db_order.status == Status.PREPARED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order has already been prepared"
        )


def ensure_order_has_not_already_been_received(db_order: Orders):
    if db_order.status == Status.RECIEVED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order is already being prepared"
        )


# Create Order
def create_order(db: Session, order: OrderCreate):
    db_order = Orders(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order(db: Session, order_id: int, order: OrderUpdate):
    db_order = get_existing_order(db, order_id)
    ensure_order_is_not_cancelled(db_order)
    ensure_order_is_not_paid_for(db_order)
    ensure_order_is_not_already_prepared(db_order)
    ensure_order_has_not_already_been_received(db_order)
    if db_order.status == Status.PENDING:
        db_order.items = order.items  # type: ignore
        db.commit()
        db.refresh(db_order)
        return db_order


def cancel_order(db: Session, order_id: int):
    db_order = get_existing_order(db, order_id)
    ensure_order_is_not_cancelled(db_order)
    ensure_order_is_not_paid_for(db_order)
    ensure_order_is_not_already_prepared(db_order)
    ensure_order_has_not_already_been_received(db_order)
    if db_order.status == Status.PENDING:
        db_order.status = Status.CANCELLED  # type: ignore
        db.commit()
        return {"Order cancelled"}


def get_orders(
    db: Session,
    offset: Optional[int] = 0,
    limit: Optional[int] = 20,
    status_: Optional[str] = None
):
    if status_:
        if status_ in (
            Status.CANCELLED, Status.PAID, Status.PENDING,
            Status.PREPARED, Status.RECIEVED
        ):
            db_orders = db.query(Orders).filter(
                Orders.status == status_).offset(offset).limit(limit).all()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{status_} is not a valid status"
            )
    db_orders = db.query(Orders).offset(offset).limit(limit).all()

    return db_orders
