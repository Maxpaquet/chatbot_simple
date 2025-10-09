from fastapi import APIRouter, Depends
from typing import Annotated, Optional, Dict, Any
from pydantic import BaseModel, Field

from langchain_core.runnables import RunnableConfig
from langgraph.types import StreamMode

from chatbot.api.lifespan import lifespan, AgentLifespanState, get_state
from chatbot.agent.answering import AnsweringState
from chatbot.api.models import ChatRequest, ThreadID
from chatbot.api.utils import prep_input, prep_config

router = APIRouter(prefix="/agent", tags=["agent"], lifespan=lifespan)


@router.post("/chat/{thread_id}")
async def agent_chat(
    thread_id: Annotated[ThreadID, "The thread ID for the conversation"],
    body: Annotated[ChatRequest, "The message from the user"],
    *,
    state: AgentLifespanState = Depends(get_state),
) -> AnsweringState:
    """Endpoint to interact with the agent in a specific thread."""

    config = prep_config(body.config, thread_id)
    input = prep_input(body.input)

    response: AnsweringState = await state.agent.astream(
        input=input,
        config=config,
        subgraphs=body.subgraphs_stream,
        stream_mode=body.stream_mode,
        durability="exit",
    )
    return response
