from typing_extensions import TypedDict
from typing import Annotated, Optional

from langgraph.graph.message import add_messages, AnyMessage


class Answer(TypedDict):
    item: str


class AnsweringState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    answer: Optional[Answer]
    remaining_steps: int
