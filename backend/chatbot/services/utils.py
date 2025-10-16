from typing import Dict, Any, Optional, List
import contextlib
import asyncio
import orjson

from langchain_core.messages import convert_to_messages
from langchain_core.load import load
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import BaseCheckpointSaver, Checkpoint
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.checkpoint.sqlite import SqliteSaver

from chatbot.services.models import ThreadID


async def prep_input(input: Dict[str, Any]) -> Dict[str, Any]:
    if "messages" in input:
        with contextlib.suppress(Exception):
            try:
                input["messages"] = convert_to_messages(input["messages"])
            except Exception:
                input["messages"] = load(input["messages"])
    return input


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
