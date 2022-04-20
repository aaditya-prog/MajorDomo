from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User

not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User does not exists"
)


def reset_password(db: Session, id: int, new_hased_password: str):
    db_user_to_update = db.query(User).filter(User.id == id).first()

    if db_user_to_update is None:
        raise not_found

    db_user_to_update.password = new_hased_password
    db.commit()
    db.refresh(db_user_to_update)

    return db_user_to_update


def get_user_by_username(db: Session, username: str):
    db_user = db.query(User).filter(User.username == username).first()

    if db_user is None:
        raise not_found

    return db_user


def create_user(db: Session, user_dict: dict):
    username = user_dict["username"]
    existing_user = db.query(User).filter(User.username == username).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with the username '{username}' "
            "already exists, pick another username."
        )

    db_user = User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
