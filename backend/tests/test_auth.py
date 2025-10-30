import asyncio
from typing import Dict

import pytest
from fastapi import HTTPException
from jose import jwt

from chatbot.auth.auth import (
    ALGORITHM,
    SECRET_KEY,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    get_user,
    verify_password,
)
from chatbot.auth.models import UserInDB


def _get_fake_db(pwd: str) -> Dict:
    """Create a fake database with one user for testing."""
    hash_wd: str = get_password_hash(pwd)
    fake_users_db: Dict = {
        "johndoe": {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": hash_wd,
            "disabled": False,
        }
    }
    return fake_users_db


def test_verify_password():
    """Test the verify_password function."""
    pwd = "mysecretpassword"
    hash_wd: str = get_password_hash(pwd)

    assert verify_password(pwd, hash_wd) is True
    assert verify_password("wrongpassword", hash_wd) is False


@pytest.mark.asyncio
async def test_get_user():
    pwd: str = "mysecretpassword"
    fake_db: Dict = _get_fake_db(pwd)

    username: str = "johndoe"
    user: UserInDB | None = await get_user(fake_db, username)
    print(user)
    assert user is not None
    assert user.username == "johndoe"
    assert user.email == "johndoe@example.com"
    assert verify_password(pwd, user.hashed_password) is True

    username: str = "notexist"
    user: UserInDB | None = await get_user(fake_db, username)
    assert user is None


@pytest.mark.asyncio
async def test_authenticate_user():
    pwd: str = "mysecretpassword"
    fake_db: Dict = _get_fake_db(pwd)
    username: str = "johndoe"

    user: UserInDB | None = await authenticate_user(
        fake_db,
        username,
        pwd,
    )
    assert user is not None
    assert user.username == "johndoe"

    user: UserInDB | None = await authenticate_user(
        fake_db,
        "notexist",
        pwd,
    )
    assert user is None

    user: UserInDB | None = await authenticate_user(
        fake_db,
        username,
        "wrongpassword",
    )
    assert user is None


@pytest.mark.asyncio
async def test_create_access_token():
    data = {"sub": "testuser"}
    token = await create_access_token(data)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "testuser"
    assert "exp" in decoded


@pytest.mark.asyncio
async def test_get_current_user_valid():
    pwd: str = "mysecretpassword"
    fake_db: Dict = _get_fake_db(pwd)
    token: str = await create_access_token({"sub": "johndoe"})

    user: UserInDB = await get_current_user(fake_db, token)
    assert isinstance(user, UserInDB)
    assert user.username == "johndoe"


@pytest.mark.asyncio
async def test_get_current_user_invalid():
    pwd: str = "mysecretpassword"
    fake_db: Dict = _get_fake_db(pwd)
    invalid_token: str = await create_access_token({"sub": "wronguser"})

    with pytest.raises(HTTPException):
        await get_current_user(fake_db, invalid_token)
