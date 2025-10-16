from typing import Dict, Any, Optional, List
import contextlib
import asyncio
import orjson

from langchain_core.messages import convert_to_messages
from langchain_core.load import load
from langchain_core.runnables import RunnableConfig

from chatbot.api.models import ThreadID


def prep_input(input: Dict[str, Any]) -> input:
    if "messages" in input:
        with contextlib.suppress(Exception):
            try:
                input["messages"] = convert_to_messages(input["messages"])
            except Exception:
                input["messages"] = load(input["messages"])
    return input


def prep_config(
    config: Optional[RunnableConfig], thread_id: ThreadID
) -> RunnableConfig:
    if config is None:
        config = RunnableConfig()
    return {
        **config,
        "configurable": {
            **config.get("configurable", {}),
            "thread_id": thread_id,
        },
    }


def _orjson_default(obj: Any) -> Any:
    """Default function for orjson to handle non-serializable objects."""
    if hasattr(obj, "model_dump") and callable(obj.model_dump):
        return obj.model_dump()
    elif hasattr(obj, "dict") and callable(obj.dict):
        return obj.dict()
    elif isinstance(obj, set | frozenset):
        return List(obj)
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
