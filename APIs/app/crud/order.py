from typing import Union
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.order import Orders
from schemas.order import OrderCreate, Status


# Create Order
def create_order(db: Session, order: OrderCreate):
    db_order = Orders(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def cancel_order(db: Session, order_id: int):
    db_order: Union[Orders, None]
    db_order = db.query(Orders).filter(Orders.order_id == order_id).first()

    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No record of such order"
        )
    elif db_order.status == Status.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order already cancelled"
        )
    elif db_order.status == Status.PAID:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order has already been paid for"
        )
    elif db_order.status == Status.PREPARED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order has already been prepared"
        )
    elif db_order.status == Status.RECIEVED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order is already being prepared"
        )
    elif db_order.status == Status.PENDING:
        db_order.status = Status.CANCELLED  # type: ignore
        db.commit()
        return {"Order cancelled"}
