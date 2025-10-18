from typing import List, Annotated, Optional

from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from langgraph.store.base import BaseStore
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph

from langgraph.prebuilt import ToolNode

from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import ToolMessage
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.tools import BaseTool, tool

from chatbot.agent.models import AnsweringState, Answer

SYSTEM_PROMPT = (
    """You are an AI assistant that helps people answering their question."""
)


async def get_tools(verbose: bool) -> List[BaseTool]:
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


async def create_agent(
    model: BaseLanguageModel,
    tools: List[BaseTool],
    name: str,
    store: Optional[BaseStore] = None,
    checkpointer: Optional[BaseCheckpointSaver] = None,
) -> CompiledStateGraph:
    """
    Creates and configures a ReAct agent with the specified language model, tools, and optional storage and checkpointing.

    Args:
        model (BaseLanguageModel): The language model to be used by the agent.
        tools (List[BaseTool]): A list of tools that the agent can utilize.
        store (Optional[BaseStore], optional): An optional storage backend for the agent's state. Defaults to None.
        checkpointer (Optional[BaseCheckpointSaver], optional): An optional checkpoint saver for persisting agent state. Defaults to None.

    Returns:
        CompiledStateGraph: The initialized and compiled agent ready for use.
    """
    kwargs = {
        "model": model,
        "tools": tools,
        "state_schema": AnsweringState,
        "prompt": SYSTEM_PROMPT,
        "name": name,
    }
    if store is not None:
        kwargs["store"] = store
    if checkpointer is not None:
        kwargs["checkpointer"] = checkpointer

    return create_react_agent(**kwargs)
