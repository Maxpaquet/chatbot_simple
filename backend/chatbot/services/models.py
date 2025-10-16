from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from enum import StrEnum

from chatbot.messages.models import MessageOut

ThreadID = str


class Thread(BaseModel):
    thread_id: ThreadID = Field(
        ..., description="The unique identifier for the thread."
    )
    channel_values: Dict[str, Any] = Field(
        ..., description="A brief description of the thread."
    )


class Language(StrEnum):
    EN = "english"
    ES = "spanish"
    FR = "french"

    @classmethod
    def default(cls) -> "Language":
        return cls.FR


class ChatRequest(BaseModel):
    thread_id: ThreadID = Field(
        ...,
        description="The thread ID for the conversation.",
    )
    input: Dict[str, Any] = Field(
        ...,
        description="The input data for the chat request.",
    )


class Thread(BaseModel):
    thread_id: ThreadID = Field(
        ...,
        description="The unique identifier for the thread.",
    )
    conversation: List[MessageOut] = Field(
        ...,
        description="The messages in the conversation.",
    )


class Event(BaseModel):
    event: str = Field(..., description="The type of event.")
    data: Optional[Any] = Field(None, description="The data associated with the event.")
