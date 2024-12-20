"""Hi
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated
from utils import get_logger

import app.services.user as user_service
import app.services.auth as auth_service
from app.routers.api import auth_middleware

from datetime import timedelta

import os

ACCESS_TOKEN_EXPIRE_HOURS = int(os.environ["AUTH_ACCESS_TOKEN_EXPIRE_HOURS"])

logger = get_logger("user_router")

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[],
    responses={},
)


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[
        user_service.UserSchema, Depends(auth_middleware.extract_user_middleware)
    ]
):
    return current_user


@router.post("/token", response_model=auth_service.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
