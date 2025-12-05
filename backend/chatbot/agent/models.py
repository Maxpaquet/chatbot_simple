from typing import Annotated, List, Optional, TypedDict

from langchain_core.documents import Document
from langgraph.graph.message import AnyMessage, add_messages
from pydantic import BaseModel, Field


class Answer(BaseModel):
    item: str = Field(..., description="The final answer to the user's question")


class AnsweringState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    answer: Optional[str]
    documents: Optional[List[Document]]
    remaining_steps: int
