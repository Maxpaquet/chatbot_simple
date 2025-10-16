from typing import Any, Dict, List, Callable

from langchain_core.runnables import RunnableConfig
from langgraph.types import StreamMode

from chatbot.services.models import ChatRequest, ThreadID, Thread
from chatbot.messages.models import MessageOut
from chatbot.api.lifespan import AgentLifespanState
from chatbot.agent.answering import AnsweringState
from chatbot.services.utils import prep_input, prep_config
from chatbot.messages.conversion import conversion_from_langchain


async def service_agent_chat(
    thread_id: ThreadID,
    body: ChatRequest,
    state: AgentLifespanState,
) -> Callable:
    print(f"[agent_chat] thread_id: {thread_id}, body: {body}")
    config: RunnableConfig = await prep_config(thread_id)
    print(f"[agent_chat] config: {config}")
    inputs: Dict[str, Any] = await prep_input(body.input)
    subgraphs_stream = True  # body.subgraphs_stream

    stream_mode: StreamMode | List[StreamMode] = ["values"]

    async def run_agent():
        last_data = None
        last_event = None
        async for item in state.agent.astream(
            input=inputs,
            config=config,
            subgraphs=subgraphs_stream,  # body.subgraphs_stream,
            stream_mode=stream_mode,
            durability="exit",
        ):

            print(f"[run_agent] item: {item}")
            if subgraphs_stream:
                graph_, event, data_ = item
            else:
                event, data_ = item
            last_event = event
            last_data = data_

        assert last_data is not None, "[run_agent] last_data is None"
        assert last_event is not None, "[run_agent] last_event is None"

        assert isinstance(last_data, dict), "[run_agent] last_data is not a dict"
        thread: Thread = await conversion_from_langchain(thread_id, last_data)
        last_message: MessageOut = thread.conversation[-1]
        sdata: Dict = last_message.serialize()
        yield f"event: {last_event}\ndata: {sdata}\n\n"

    return run_agent
