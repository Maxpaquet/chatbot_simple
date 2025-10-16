from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from enum import StrEnum

from langchain_core.runnables import RunnableConfig
from langgraph.types import StreamMode
from langchain_core.messages import BaseMessage

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


class RunnableConfigChat(RunnableConfig):
    language: Language = Field(
        default=Language.default(), description="The language for the chat."
    )


class ChatRequest(BaseModel):
    input: Dict[str, Any] = Field(
        ..., description="The input data for the chat request."
    )
    # use a factory to avoid creating a single shared instance at import time
    config: RunnableConfigChat = Field(
        default_factory=RunnableConfigChat,
        description="Configuration for the runnable.",
    )
    subgraphs_stream: bool = Field(
        True, description="Whether to stream subgraphs in the response."
    )
    # use default_factory for mutable defaults (lists)
    stream_mode: StreamMode | List[StreamMode] = Field(
        ["values"], description="The streaming mode for the response."
    )
