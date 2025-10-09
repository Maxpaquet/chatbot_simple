from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from langchain_core.runnables import RunnableConfig
from langgraph.types import StreamMode

ThreadID = str


class Thread(BaseModel):
    thread_id: ThreadID = Field(
        ..., description="The unique identifier for the thread."
    )
    channel_values: Dict[str, Any] = Field(
        ..., description="A brief description of the thread."
    )


class ChatRequest(BaseModel):
    input: Dict[str, Any] = Field(
        ..., description="The input data for the chat request."
    )
    config: Optional[RunnableConfig] = Field(
        None, description="Configuration for the runnable."
    )
    subgraphs_stream: Optional[bool] = Field(
        True, description="Whether to stream subgraphs in the response."
    )
    stream_mode: StreamMode = Field(
        "values", description="The streaming mode for the response."
    )
