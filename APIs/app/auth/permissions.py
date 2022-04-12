from fastapi import Depends, HTTPException, status

from auth import AuthHandler
from models.user import User as ModelUser
from schemas.user import Staff


def ensure_is_admin(
    current_user: ModelUser = Depends(AuthHandler.auth_wrapper)
):
    if current_user.staff != Staff.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )

    return current_user
