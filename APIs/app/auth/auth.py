from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import database

from crud.user import get_user_by_username
from models.user import User as ModelUser


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = "SECRET"

    @classmethod
    def get_password_hash(cls, password):
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def check_password(cls, password, hash_password) -> str:
        return cls.pwd_context.verify(password, hash_password)

    # Function to encode the JWT Token
    @classmethod
    def encode_token(cls, user_id):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, hours=12),
            "iat": datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(payload, cls.secret, algorithm="HS256")

    # Function to decode the JWT Token
    @classmethod
    def decode_token(cls, token):
        try:
            payload = jwt.decode(token, cls.secret, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    @classmethod
    def auth_wrapper(
        cls,
        auth: HTTPAuthorizationCredentials = Security(security),
        db: Session = Depends(get_db)
    ):
        username = cls.decode_token(auth.credentials)

        user: ModelUser = get_user_by_username(db, username)

        return user

    # Function to validate the password
    @staticmethod
    def validate_password(passwd):

        special_sym = ["$", "@", "#", "%", "!", "&"]
        val = True

        if len(passwd) < 6:
            val = False

        if len(passwd) > 20:
            val = False

        if not any(char.isdigit() for char in passwd):
            val = False

        if not any(char.isupper() for char in passwd):
            val = False

        if not any(char.islower() for char in passwd):
            val = False

        if not any(char in special_sym for char in passwd):
            val = False
        if val:
            return val
