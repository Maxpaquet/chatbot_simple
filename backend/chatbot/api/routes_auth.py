from typing import Dict

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from chatbot.auth.auth import get_current_active_user
from chatbot.auth.db import fake_users_db
from chatbot.auth.models import User
from chatbot.services.auth import service_login_for_access_token

router_login = APIRouter()


@router_login.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return access token."""
    dict_access_token: Dict[str, str] = await service_login_for_access_token(
        form_data, fake_users_db
    )
    return dict_access_token


@router_login.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router_login.get("/protected")
async def protected_route(current_user: User = Depends(get_current_active_user)):
    """A protected route that requires authentication."""
    return {"message": f"Hello, {current_user.username}! This is a protected route."}
