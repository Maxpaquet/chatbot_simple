from typing import Annotated, List, Optional

from langchain_core.documents import Document
from langgraph.graph.message import AnyMessage, add_messages
from typing_extensions import TypedDict


class Answer(TypedDict):
    item: str


class AnsweringState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    answer: Optional[str]
    documents: Optional[List[Document]]
    remaining_steps: int
