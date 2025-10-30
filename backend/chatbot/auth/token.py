from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from jose import jwt

from chatbot.auth.models import UserInDB
from chatbot.auth.utils import ALGORITHM, SECRET_KEY


def create_token(user: UserInDB) -> Dict[str, str]:
    """Create a simple token dictionary (not JWT)."""
    return {"sub": f"username:{user.username}"}


def sub_to_username(sub: str) -> str:
    """Extract username from the 'sub' field."""
    prefix = "username:"
    if sub.startswith(prefix):
        return sub[len(prefix) :]
    raise ValueError("Invalid subject format")


async def create_access_token(
    data: Dict, expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token."""
    to_encode: Dict = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
