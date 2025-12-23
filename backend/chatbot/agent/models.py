from typing import Annotated, List, Optional

from langchain_core.documents import Document
from langgraph.graph.message import BaseMessage, add_messages
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class Answer(BaseModel):
    item: str = Field(..., description="The final answer to the user's question")


class AnsweringState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    answer: Optional[str]
    documents: Optional[List[Document]]
    remaining_steps: int
