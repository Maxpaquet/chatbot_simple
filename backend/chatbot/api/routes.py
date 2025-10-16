from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from typing import Annotated, Optional, Dict, Any
from pydantic import BaseModel, Field

from langchain_core.runnables import RunnableConfig
from langgraph.types import StreamMode

from chatbot.api.lifespan import lifespan, AgentLifespanState, get_state
from chatbot.agent.answering import AnsweringState
from chatbot.api.models import ChatRequest, ThreadID
from chatbot.api.utils import prep_input, prep_config, serialize_data

router = APIRouter(prefix="/agent", tags=["agent"], lifespan=lifespan)


@router.post("/chat/{thread_id}")
async def agent_chat(
    thread_id: Annotated[ThreadID, "The thread ID for the conversation"],
    body: Annotated[ChatRequest, "The message from the user"],
    *,
    state: AgentLifespanState = Depends(get_state),
) -> StreamingResponse:
    """Endpoint to interact with the agent in a specific thread."""
    print(f"[agent_chat] thread_id: {thread_id}, body: {body}")
    config = prep_config(body.config, thread_id)
    print(f"[agent_chat] config: {config}")
    inputs: Dict[str, Any] = prep_input(body.input)
    subgraphs_stream = True  # body.subgraphs_stream

    async def run_agent():
        async for item in state.agent.astream(
            input=inputs,
            config=config,
            subgraphs=subgraphs_stream,  # body.subgraphs_stream,
            stream_mode=body.stream_mode,
            durability="exit",
        ):
            print(f"[run_agent] item: {item}")
            if subgraphs_stream:
                graph_, event, data = item
            else:
                event, data = item
            sdata = await serialize_data(data)
            # print(f"event: {event}, data: {sdata}")
            yield f"event: {event}\ndata: {sdata}\n\n"

    return StreamingResponse(run_agent(), media_type="text/event-stream")
