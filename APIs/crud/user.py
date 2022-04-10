from sqlalchemy.orm import Session

from models.user import User


def reset_password(db: Session, id: int, new_hased_password: str):
    db_user_to_update = db.query(User).filter(User.id == id).first()
    if db_user_to_update:
        db_user_to_update.password = new_hased_password
        db.commit()
        db.refresh(db_user_to_update)
    return db_user_to_update


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user_dict: dict):
    db_user = User(user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
