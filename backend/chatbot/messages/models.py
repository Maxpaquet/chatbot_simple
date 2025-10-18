from typing import Dict
from pydantic import BaseModel, Field
from enum import StrEnum
from datetime import date


class Author(StrEnum):
    user = "user"
    agent = "agent"
    tool = "tool"
    system = "system"


class MessageIn(BaseModel):
    id: str = Field(..., description="The unique identifier for the message.")
    author: Author = Field(
        ..., description="The author of the message (e.g., user, assistant)."
    )
    content: str = Field(..., description="The content of the message.")


class MessageOut(MessageIn):
    id: str = Field(..., description="The unique identifier for the message.")
    timestamp: date = Field(
        ...,
        description="The timestamp when the message was created.",
    )
    author: Author = Field(
        ...,
        description="The author of the message (e.g., user, assistant).",
    )
    content: str = Field(..., description="The content of the message.")

    def serialize(self) -> Dict:
        return {
            "id": self.id,
            "author": self.author.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
        }

    def __str__(self) -> str:
        return f"[{self.timestamp.isoformat()}] {self.author.value}: {self.content}"
