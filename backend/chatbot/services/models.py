from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from enum import StrEnum

from chatbot.messages.models import MessageOut, MessageIn

ThreadID = str


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
    input: MessageIn = Field(
        ...,
        description="The input data for the chat request.",
    )
    agent_id: Optional[str] = Field(
        None,
        description="The ID of the agent to chat with.",
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

    def __str__(self) -> str:
        conv_str = "\n".join(str(msg) for msg in self.conversation)
        return f"Thread ID: {self.thread_id}\nConversation:\n{conv_str}"


class Event(BaseModel):
    event: str = Field(..., description="The type of event.")
    data: Optional[Any] = Field(None, description="The data associated with the event.")


class AgentNames(BaseModel):
    names: List[str] = Field(..., description="List of agent names.")