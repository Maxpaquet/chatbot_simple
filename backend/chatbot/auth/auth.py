from typing import Any, Dict

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from chatbot.auth.db import fake_users_db
from chatbot.auth.models import User, UserInDB
from chatbot.auth.token import sub_to_username
from chatbot.auth.utils import (
    ALGORITHM,
    MAX_LEN_CRYPT,
    OAUTH2_SCHEME,
    PWD_CONTEXT,
    SECRET_KEY,
)


def verify_password(plain_password: str | bytes, hashed_password: str | bytes) -> bool:
    """Verify a password against its hash."""
    verification: bool = PWD_CONTEXT.verify(plain_password, hashed_password)
    return verification


def get_password_hash(password: str) -> str:
    """Generate a hash for a password."""
    return PWD_CONTEXT.hash(password[:MAX_LEN_CRYPT])


async def get_user(db: Dict, username: str) -> UserInDB | None:
    """Get a user from the database."""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    else:
        return None


async def authenticate_user(
    db: Dict,
    username: str,
    password: str,
) -> UserInDB | None:
    """Check if username and password are correct."""
    user: UserInDB | None = await get_user(db, username)
    if user is None:
        return None
    password_verified: bool = verify_password(password, user.hashed_password)
    if not password_verified:
        return None
    return user


async def get_current_user(token: str = Depends(OAUTH2_SCHEME)) -> UserInDB:
    """Get the current user from the JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    db = fake_users_db

    try:
        payload: Dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None or not isinstance(sub, str):
            raise credentials_exception
        username: str = sub_to_username(sub)
    except JWTError:
        raise credentials_exception

    user: UserInDB | None = await get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: UserInDB = Depends(get_current_user),
) -> User:
    """Get the current active user (not disabled)."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    # Convert UserInDB to User (exclude hashed_password)
    retrieved_user: User = current_user.to_user()

    return retrieved_user
    return retrieved_user
