import logging
import time

from jose import jwt

from decouple import config

from fastapi import Request
from fastapi import HTTPException

from fastapi.security import HTTPBearer

log = logging.getLogger(__name__)


class JWTBearer(HTTPBearer):
    JWT_SECRET = config("jwt_secret")
    JWT_ALGORITHM = config("jwt_algorithm")

    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        if credentials := await self.get_credentials(request):
            if not self.verify_jwt(credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    async def get_credentials(self, request: Request):
        if session_token := request.cookies.get("session"):
            return session_token
        try:
            return (await super().__call__(request)).credentials
        except AttributeError:
            return None

    def verify_jwt(self, jwt_token: str) -> bool:
        token_is_valid: bool = False

        try:
            payload = self.decode_jwt(jwt_token)
        except Exception:
            payload = None

        if payload:
            token_is_valid = True
        return token_is_valid

    @staticmethod
    def token_response(token: str, expires: float):
        return {
            "token": token,
            "expires": expires
        }

    @classmethod
    def sign_jwt(cls, user_id: str, expiry_time_seconds: int = 600) -> dict:
        expiry_time = expiry_time_seconds + time.time()

        payload = {
            "user_id": user_id,
            "expires": expiry_time + time.time()
        }
        token = jwt.encode(payload, cls.JWT_SECRET, algorithm=cls.JWT_ALGORITHM)

        return cls.token_response(token, expiry_time)

    @classmethod
    def decode_jwt(cls, token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, cls.JWT_SECRET, algorithms=[cls.JWT_ALGORITHM])
            return decoded_token if decoded_token["expires"] >= time.time() else None
        except Exception as error:
            log.error(error)
            return {}
