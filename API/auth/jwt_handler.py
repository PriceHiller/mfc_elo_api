import logging
import time

from jose import jwt

from decouple import config

from API import root_path

env_path = root_path.__str__()
JWT_SECRET = config("jwt_secret")
JWT_ALGORITHM = config("jwt_algorithm")

log = logging.getLogger(__name__)


def token_response(token: str):
    return {
        "access_token": token
    }


def sign_jwt(user_id: str, expiry_time_seconds: int = 600) -> dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + expiry_time_seconds
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as error:
        log.error(error)
        return {}
