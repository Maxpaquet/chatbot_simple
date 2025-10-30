from typing import Annotated, Callable

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from chatbot.api.lifespan import AgentLifespanState, get_state, lifespan
from chatbot.services.chat import service_agent_chat
from chatbot.services.models import AgentNames, ChatRequest, Event, Thread, ThreadID
from chatbot.services.thread import service_get_agents_name, service_get_thread

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


@router.get("/list/agents", response_model=AgentNames)
async def get_agents(*, state: AgentLifespanState = Depends(get_state)) -> AgentNames:
    """Endpoint to list all available agents."""
    agent_names: AgentNames = await service_get_agents_name(state.agent_dict)
    return agent_names
