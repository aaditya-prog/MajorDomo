from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..auth.authentication import AuthHandler
from ..auth.permissions import ensure_is_admin
from ..config import database
from ..crud.user import create_user, get_user_by_username, reset_password
from ..models.user import User as ModelUser
from ..schemas.user import ChangePassword, User, UserCreate
from ..schemas.token import Token

router = APIRouter(prefix="/user", tags=["User"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
 API Endpoints for "user" submodule.

"""


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
    dependencies=[Depends(ensure_is_admin)]
)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Use "validate_password" function from "Auth_Handler" class
    # to check password combinations, throw exception if
    # the combinations are bad.
    if not AuthHandler.validate_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Password not accepted. It must contain one uppercase "
                "letter, one lowercase letter, one numeral, "
                "one special character and should be longer "
                "than 6 characters and shorter than 20 characters"
            )
        )

    user_dict = user.dict()
    user_dict["password"] = AuthHandler.get_password_hash(user.password)
    db_user = create_user(db, user_dict)
    return db_user


@router.post("/auth/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Use "get_user_by_username" function to get user from the database.
    user_db = get_user_by_username(db, form_data.username)

    # If user doesn't exist in database, raise an exception.
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f" User '{form_data.username}' doesn't exist, try again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    password = user_db.password
    verify_password = AuthHandler.verify_password(
        form_data.password, password
    )
    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Password, try again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username = user_db.username
    token = AuthHandler.encode_token(username)
    return {"token": token, "token_type": "Bearer"}


@router.get("/profile", response_model=User)
def profile(
    current_user: ModelUser = Depends(AuthHandler.auth_wrapper)
):
    return current_user


@router.patch("/change-password")
async def change_password(
    passwords: ChangePassword,
    current_user: ModelUser = Depends(AuthHandler.auth_wrapper),
    db: Session = Depends(get_db),
):
    if not AuthHandler.validate_password(passwords.new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Password not accepted. It must contain one uppercase "
                "letter, one lowercase letter, one numeral, "
                "one special character and should be longer "
                "than 6 characters and shorter than 20 characters"
            )
        )

    password = current_user.password

    verify_password = AuthHandler.check_password(
        passwords.old_password, password
    )

    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not verify password, try again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if passwords.new_password != passwords.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and Confirm Password do not match"
        )
    new_password_hash = AuthHandler.get_password_hash(
        passwords.new_password
    )
    user = User.from_orm(current_user)
    reset_password(db, user.id, new_password_hash)

    return {
        "message": f"Password updated for the user: {current_user.username}"
    }
