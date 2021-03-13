from fastapi import Depends
from fastapi import HTTPException

from bcrypt import hashpw
from bcrypt import gensalt
from bcrypt import checkpw
from fastapi.security import APIKeyCookie

from API.auth import jwt

JWTBearer = jwt.JWTBearer

users = []

SESSION_COOKIE = APIKeyCookie(name="session")


def _handle_token(token: str):
    payload = JWTBearer.decode_jwt(token)
    for existing_user in users:
        if existing_user.email == payload.get("user_id"):
            return existing_user
    return None


def _jwt_token(token: str = Depends(JWTBearer())):
    return _handle_token(token)


async def check_authentication(token: str = Depends(_jwt_token)):
    if token:
        return token
    raise HTTPException(
        status_code=403
    )


def verify_password(plain_password: [str, bytes], hashed_password: [str, bytes]):
    if not isinstance(plain_password, bytes):
        plain_password = plain_password.encode("utf8")
    if not isinstance(hashed_password, bytes):
        hashed_password = hashed_password.encode("utf8")
    return checkpw(plain_password, hashed_password)


def get_password_hash(password: [str, bytes]):
    if not isinstance(password, bytes):
        password = password.encode("utf8")
    return hashpw(password, gensalt())


__all__ = [
    "JWTBearer",
    "check_authentication",
    "verify_password",
    "get_password_hash"
]
