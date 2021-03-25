import os
import logging

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from jose import jwt

from fastapi import Request
from fastapi import Response
from fastapi import HTTPException

from fastapi.security import HTTPBearer

log = logging.getLogger(__name__)


class JWTBearer(HTTPBearer):
    JWT_SECRET = os.getenv("jwt_secret").strip()
    if not JWT_SECRET:
        raise AttributeError(f"JWT_SECRET does not have an environment variable: \"jwt_secret\"")

    JWT_ALGORITHM = os.getenv("jwt_algorithm")
    if not JWT_ALGORITHM:
        raise AttributeError(f"JWT_ALGORITHM does not have an environment variable: \"jwt_algorithm\"")

    timezone = timezone.utc

    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        if credentials := await self.get_credentials(request):
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            user_id: int = self.decode_jwt(credentials.credentials)["user_id"]
            log.info(f"Successful authentication for user id \"{user_id}\" with token: \"{credentials.credentials}\"")
            return credentials, user_id
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    async def get_credentials(self, request: Request):
        if not request.scope.get("authorization"):
            if session_token := request.cookies.get("session"):
                if self.verify_jwt(session_token):
                    request.scope["headers"].append((b'authorization', session_token.encode()))
        return await super(JWTBearer, self).__call__(request)

    @classmethod
    def verify_jwt(cls, jwt_token: str) -> bool:
        token_is_valid: bool = False

        try:
            payload = cls.decode_jwt(jwt_token)

        except Exception:
            payload = None

        if payload:
            token_is_valid = True
        return token_is_valid

    @classmethod
    def sign_jwt(cls, user_id: [str, id], expiry_time: timedelta = timedelta(days=180), remove_bearer=False) -> str:

        expiry_time = str(datetime.now(tz=cls.timezone) + expiry_time)

        log.info(f"Issued a token for user_id: \"{user_id}\" that expires \"{expiry_time}\"")
        payload = {
            "user_id": str(user_id),
            "expires": expiry_time
        }
        encoded_token = jwt.encode(payload, cls.JWT_SECRET, algorithm=cls.JWT_ALGORITHM)
        if remove_bearer:
            token = encoded_token
        else:
            token = "Bearer " + encoded_token

        return token

    @classmethod
    def decode_jwt(cls, token: str) -> dict:
        token = token.replace("Bearer ", "")
        try:
            decoded_token = jwt.decode(token, cls.JWT_SECRET, algorithms=[cls.JWT_ALGORITHM])
            expiry_time = datetime.fromisoformat(decoded_token["expires"])
            return decoded_token if expiry_time >= datetime.now(tz=cls.timezone) else None
        except Exception as error:
            log.error(error)
            return {}

    @staticmethod
    async def grant_cookie(response: Response, token: str):
        response.set_cookie("session", token)

    @staticmethod
    async def remove_cookie(response: Response):
        cookie = response.headers.get("session")
        response.delete_cookie("session")
        return cookie

    @staticmethod
    async def get_cookie_from_header(response: Response):
        return response.headers.get("session")
