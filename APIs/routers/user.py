from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from auth import AuthHandler
from schemas.user import ChangePassword, User, UserCreate

import database

router = APIRouter(prefix="/user")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# An instance of AuthHandler class
# from auth.py which contains authentication functions.
auth_handler = (AuthHandler())

"""
 API Endpoints for "user" submodule.

"""


@router.post(
    "/register",
    status_code=201,
    response_model=User,
    tags=["User CRUD"]
)
async def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):

    # Use "validate_password" function from "Auth_Handler" class
    # to check password combinations, throw exception if
    # the combinations are bad.
    if not auth_handler.validate_password(user.password):
        raise HTTPException(
            status_code=401,
            detail=(
                "Password not accepted. It must contain one uppercase "
                "letter, one lowercase letter, one numeral, "
                "one special character and should be longer "
                "than 6 characters and shorter than 20 characters"
            )
        )

    # Use "get_user_by_username" function to get user from the database.
    user_db = auth_handler.get_user_by_username(db, username=user.username)

    # If the entered username exists in db, raise exception.
    if user_db:
        raise HTTPException(
            status_code=400,
            detail=(
                f"User with the username '{user.username}' "
                "already exists, pick another username."
            )
        )

    # If username is unique, save details in database.
    if user_db is None:
        db_user = auth_handler.create_user(db=db, user=user)
        return db_user


@router.post("/auth/login", tags=["Common APIs"])
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Use "get_user_by_username" function to get user from the database.
    user_db = auth_handler.get_user_by_username(db, form_data.username)

    # If user doesn't exist in database, raise an exception.
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f" User '{form_data.username}' doesn't exist, try again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    password = user_db.password
    verify_password = auth_handler.verify_password(
        form_data.password, password
    )
    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Password, try again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username = user_db.username
    token = auth_handler.encode_token(username)
    return {"token": token, "token_type": "Bearer"}


@router.get("/profile", tags=["Common APIs"])
def profile(
    username=Depends(auth_handler.auth_wrapper),
    db: Session = Depends(get_db)
):
    current_user = auth_handler.get_user_by_username(db, username)
    username = current_user.username
    full_name = current_user.full_name
    staff_type = current_user.staff_type
    return JSONResponse(
        status_code=200,
        content={
            "username": username, "full_name": full_name, "Role": staff_type
        }
    )


@router.patch("/change-password", tags=["Common APIs"])
async def change_password(
    reset_password: ChangePassword,
    username=Depends(auth_handler.auth_wrapper),
    db: Session = Depends(get_db),
):
    current_user = auth_handler.get_user_by_username(db, username=username)

    password = current_user.password
    verify_password = auth_handler.check_password(
        reset_password.old_password, password
    )

    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not verify password, try again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if reset_password.new_password != reset_password.confirm_password:
        raise HTTPException(
            status_code=404,
            detail="New password and Confirm Password do not match"
        )
    auth_handler.check_reset_password(
        reset_password.new_password, current_user.id, db
    )

    return {
        "message": f"Password updated for the user: {current_user.username}"
    }
