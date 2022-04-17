from fastapi import Depends, HTTPException, status

from .authentication import AuthHandler
from models.user import User as ModelUser
from schemas.user import Staff


unauthorized_error = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not authorized to perform this action"
)


def ensure_is_admin(
    current_user: ModelUser = Depends(AuthHandler.auth_wrapper)
):
    if current_user.staff != Staff.ADMIN:
        raise unauthorized_error

    return current_user


def ensure_cashier_or_kitchen_staff(
    current_user: ModelUser = Depends(AuthHandler.auth_wrapper)
):
    if current_user.staff not in (Staff.CASHIER, Staff.KITCHEN_STAFF):
        raise unauthorized_error

    return current_user


def ensure_is_inventory_staff(
    current_user: ModelUser = Depends(AuthHandler.auth_wrapper)
):
    if current_user.staff != Staff.INVENTORY_STAFF:
        raise unauthorized_error

    return current_user


def ensure_is_kitchen_staff(
    current_user: ModelUser = Depends(AuthHandler.auth_wrapper)
):
    if current_user != Staff.KITCHEN_STAFF:
        raise unauthorized_error

    return current_user
