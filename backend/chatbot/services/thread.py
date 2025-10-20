from typing import Dict, Any, List

from langgraph.pregel import Pregel
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.checkpoint.sqlite import SqliteSaver

from chatbot.services.models import ChatRequest, ThreadID, Thread, AgentNames
from chatbot.services.utils import get_agent_state
from chatbot.messages.conversion import conversion_from_langchain


async def service_get_thread(
    thread_id: ThreadID,
    checkpointer: AsyncSqliteSaver | SqliteSaver,
) -> Thread:
    """Retrieve a thread by its ID."""
    state: Dict[str, Any] | None = await get_agent_state(thread_id, checkpointer)
    if state is None:
        return Thread(thread_id=thread_id, conversation=[])
    thread: Thread = await conversion_from_langchain(thread_id, state)
    return thread


async def service_get_agents_name(agents_dict: Dict[str, Pregel]) -> AgentNames:
    """Retrieve the names of all available agents."""
    names: List[str] = list(agents_dict.keys())
    return AgentNames(names=names)
