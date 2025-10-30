from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str

    def to_user(self) -> User:
        return User(
            username=self.username,
            email=self.email,
            full_name=self.full_name,
            disabled=self.disabled
        )


class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
