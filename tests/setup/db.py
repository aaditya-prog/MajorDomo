from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.auth.authentication import AuthHandler
from app.models.user import User
from app.schemas.user import Staff

DATABASE_URL = "sqlite:///./majordomotest.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)

TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def generate_dummy_user(word: str):
    return {
        "username": word.title(),
        "full_name": word.title(),
        "password": word.title() + "1234!",
        "staff": word.title()
    }


def get_test_session():
    test_db = TestingSession()
    try:
        yield test_db
    finally:
        test_db.close()


def create_admin():
    user_copy = generate_dummy_user(Staff.ADMIN)
    hashed_password = AuthHandler.get_password_hash(user_copy["password"])
    user_copy["password"] = hashed_password
    db_user = User(**user_copy)
    db: Session = TestingSession()
    try:
        admin = db.query(User).filter(
            User.username == user_copy["username"]
        ).first()
        if admin is None:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
    finally:
        db.close()
    return db_user
