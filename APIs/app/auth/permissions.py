from fastapi import Depends, HTTPException, status

from auth import AuthHandler
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


def ensure_can_view_order(
    current_user: ModelUser = Depends(AuthHandler.auth_wrapper)
):
    if current_user.staff not in (Staff.CASHIER, Staff.KITCHEN_STAFF):
        raise unauthorized_error

    return current_user
