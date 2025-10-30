from datetime import timedelta
from typing import Dict

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from chatbot.auth.auth import authenticate_user
from chatbot.auth.models import UserInDB
from chatbot.auth.token import create_access_token, create_token
from chatbot.auth.utils import ACCESS_TOKEN_EXPIRE_MINUTES


async def service_login_for_access_token(
    form_data: OAuth2PasswordRequestForm, db: Dict
) -> Dict[str, str]:
    """Authenticate user and return access token."""
    user: UserInDB | None = await authenticate_user(
        db, form_data.username, form_data.password
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token: str = await create_access_token(
        data=create_token(user),
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
