from typing import Dict, Any, Optional
import contextlib

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
