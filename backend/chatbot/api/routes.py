from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from typing import Annotated, Dict, Any, List, Callable


from chatbot.api.lifespan import lifespan, AgentLifespanState, get_state

from chatbot.services.models import ChatRequest, ThreadID, Thread
from chatbot.services.models import Event

from chatbot.services.chat import service_agent_chat
from chatbot.services.thread import service_get_thread

router = APIRouter(prefix="/agent", tags=["agent"], lifespan=lifespan)


@router.post("/chat/{thread_id}", response_model=Event)
async def agent_chat(
    thread_id: Annotated[ThreadID, "The thread ID for the conversation"],
    body: Annotated[ChatRequest, "The message from the user"],
    *,
    state: AgentLifespanState = Depends(get_state),
) -> StreamingResponse:
    """Endpoint to interact with the agent in a specific thread."""
    run_agent: Callable = await service_agent_chat(thread_id, body, state)
    return StreamingResponse(run_agent(), media_type="text/event-stream")


@router.get("/chat/thread/{thread_id}", response_model=Thread)
async def get_thread_messages(
    thread_id: Annotated[ThreadID, "The thread ID for the conversation"],
    *,
    state: AgentLifespanState = Depends(get_state),
) -> Thread:
    """Endpoint to retrieve messages from a specific thread."""
    thread: Thread = await service_get_thread(thread_id, state.checkpointer)
    return thread
