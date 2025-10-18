from typing_extensions import TypedDict
from typing import Annotated, Optional, List

from langgraph.graph.message import add_messages, AnyMessage
from langchain_core.messages import BaseMessage


class Answer(TypedDict):
    item: str


class AnsweringState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    answer: Optional[Answer]
    remaining_steps: int
