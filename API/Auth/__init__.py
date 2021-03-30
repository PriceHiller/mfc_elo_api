from fastapi import Depends
from fastapi import HTTPException

from bcrypt import hashpw
from bcrypt import gensalt
from bcrypt import checkpw
from fastapi.security import APIKeyCookie

from API.Auth import jwt

JWTBearer = jwt.JWTBearer


def verify_password(plain_password: [str, bytes], hashed_password: [str, bytes]):
    if not isinstance(plain_password, bytes):
        plain_password = plain_password.encode("utf8")
    if not isinstance(hashed_password, bytes):
        hashed_password = hashed_password.encode("utf8")
    return checkpw(plain_password, hashed_password)


def get_password_hash(password: [str, bytes]) -> str:
    if not isinstance(password, bytes):
        password = password.encode("utf8")
    return hashpw(password, gensalt()).decode("utf8")


__all__ = [
    "JWTBearer",
    "verify_password",
    "get_password_hash"
]
