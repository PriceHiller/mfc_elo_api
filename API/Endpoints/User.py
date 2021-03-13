from datetime import timedelta

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status

from API.Schemas.auth import fake_users_db
from API.Schemas.auth.token import Token
from API.Schemas.auth.user import authenticate_user, create_access_token, get_current_active_user, User
from API.auth import ACCESS_TOKEN_EXPIRES_MINUTES
from API.Endpoints import BaseEndpoint


class Example(BaseEndpoint):
    route = APIRouter()

    @staticmethod
    @route.post("/token", response_model=Token)
    async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
        user = authenticate_user(fake_users_db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    @route.get("/users/me/", response_model=User)
    async def read_users_me(current_user: User = Depends(get_current_active_user)):
        return current_user

    @staticmethod
    @route.get("/users/me/items/")
    async def read_own_items(current_user: User = Depends(get_current_active_user)):
        return [{"item_id": "Foo", "owner": current_user.username}]
