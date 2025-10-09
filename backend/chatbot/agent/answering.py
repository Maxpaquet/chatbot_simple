from typing import List, Annotated, Optional
from typing_extensions import TypedDict

from langgraph.prebuilt import create_react_agent
from langgraph.graph.message import add_messages, AnyMessage
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from langgraph.store.base import BaseStore
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph

from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import ToolMessage
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.tools import BaseTool, tool

SYSTEM_PROMPT = (
    """You are an AI assistant that helps people answering their question."""
)


class Answer(TypedDict):
    item: str


class AnsweringState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    answer: Optional[Answer]
    remaining_steps: int


def get_tools(verbose: bool) -> List[BaseTool]:
    @tool
    def answer(
        reasoning: Annotated[
            str, "The reasoning behind choosing this tool with the argument"
        ],
        final_answer: Annotated[Answer, "The final answer to the question of the user"],
        state: Annotated[AnsweringState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ):
        """Use this function to formulate the final answer when you have all the documentation to answer."""
        if verbose:
            print(
                f"[formulate_answer] final_answer={str(final_answer)}\nreasoning: {reasoning}"
            )
        return Command(
            update={
                "answer": final_answer,
                "messages": [
                    ToolMessage(
                        content=str(final_answer),
                        artifact=final_answer,
                        tool_call_id=tool_call_id,
                    )
                ],
            }
        )

    return [answer]


def create_agent(
    model: BaseLanguageModel,
    tools: List[BaseTool],
    store: Optional[BaseStore] = None,
    checkpointer: Optional[BaseCheckpointSaver] = None,
) -> CompiledStateGraph:
    kwargs = {
        "model": model,
        "tools": tools,
        "state_schema": AnsweringState,
        "prompt": SYSTEM_PROMPT,
    }
    if store is not None:
        kwargs["store"] = store
    if checkpointer is not None:
        kwargs["checkpointer"] = checkpointer

    return create_react_agent(**kwargs)
