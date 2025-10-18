from typing import Dict, Any, Optional, List
import contextlib
import asyncio
import orjson

from langchain_core.messages import convert_to_messages
from langchain_core.load import load
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage

from langgraph.checkpoint.base import BaseCheckpointSaver, Checkpoint
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import AnyMessage

from chatbot.messages.models import MessageIn
from chatbot.services.models import ThreadID
from chatbot.agent.answering import AnsweringState


async def prep_input(message: MessageIn) -> AnsweringState:
    # if "messages" in message:
    #     with contextlib.suppress(Exception):
    #         try:
    #             message["messages"] = convert_to_messages(message["messages"])
    #         except Exception:
    #             message["messages"] = load(message["messages"])
    messages: List[AnyMessage] = [
        HumanMessage(
            content=message.content,
            id=message.id,
        )
    ]
    prep_input = AnsweringState(
        messages=messages,
        answer=None,
        remaining_steps=10,
    )
    return prep_input


async def prep_config(thread_id: ThreadID) -> RunnableConfig:
    return {"configurable": {"thread_id": thread_id}}


async def get_agent_state(
    thread_id: ThreadID,
    checkpointer: AsyncSqliteSaver | SqliteSaver,
) -> Dict[str, Any] | None:
    """Retrieve the last state of the agent from the checkpointer."""
    config: RunnableConfig = {"configurable": {"thread_id": thread_id}}

    ckeckpoint: Checkpoint | None = (
        await checkpointer.aget(config)
        if isinstance(checkpointer, AsyncSqliteSaver)
        else checkpointer.get(config)
    )
    if ckeckpoint is None:
        return None
    return ckeckpoint.get("channel_values", None)


def _orjson_default(obj: Any) -> Any:
    """Default function for orjson to handle non-serializable objects."""
    if hasattr(obj, "model_dump") and callable(obj.model_dump):
        return obj.model_dump()
    elif hasattr(obj, "dict") and callable(obj.dict):
        return obj.dict()
    elif isinstance(obj, set | frozenset):
        return list(obj)
    else:
        raise TypeError(
            f"Object of type {obj.__class__.__name__} is not JSON serializable"
        )


async def serialize_data(data: Any) -> str:
    """Serialize data to a string for streaming."""
    if isinstance(data, str):
        return data
    return await asyncio.get_running_loop().run_in_executor(
        None,
        lambda e=data: orjson.dumps(
            e,
            default=_orjson_default,
            option=orjson.OPT_NON_STR_KEYS,
        ).decode(),
    )
