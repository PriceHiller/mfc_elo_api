from fastapi import APIRouter, Depends
from fastapi import Body
from fastapi import Response
from fastapi import Request
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session

from API.Endpoints import BaseEndpoint

from API.Schemas.user import User as SchemaUser
from API.Schemas.user import UserPW

from API.auth import JWTBearer
from API.auth import verify_password

from API.Database import get_db
from API.Database.crud.user import create_user
from API.Database.crud.user import get_user_by_username


class User(BaseEndpoint):
    route = APIRouter(prefix="/user")

    tags = ["user"]

    @staticmethod
    @route.post("/signup", tags=tags)
    async def create_user(response: Response, user: UserPW = Body(...), db: Session = Depends(get_db)):
        create_user(db=db, user=user)
        return {"Status": "User Created"}

    @staticmethod
    @route.post("/login", tags=tags)
    async def login_user(response: Response, request: Request, user: UserPW = Body(...), db=Depends(get_db)):
        if existing_user := get_user_by_username(db=db, username=user.username):
            if existing_user.username == user.username and \
                    verify_password(user.password, existing_user.hashed_password):
                jwt = JWTBearer.sign_jwt(user.username)
                await JWTBearer.grant_cookie(response, jwt)
                return {"token": jwt}
        raise HTTPException(status_code=403,
                            detail="Incorrect Login Credentials")

    @staticmethod
    @route.post("/verify", tags=tags)
    async def read_private(user: SchemaUser = Depends(JWTBearer())):
        return {"username": user, "user status": "good"}
