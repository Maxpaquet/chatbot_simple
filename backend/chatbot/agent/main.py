from typing import Dict, Optional

from langgraph.store.base import BaseStore
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.pregel import Pregel
from chatbot.agent.answering import create_agent, get_tools
from chatbot.utils import aget_model


async def get_agent(
    checkpointer: Optional[BaseCheckpointSaver],
    verbose: bool = False,
    mock: bool = False,
) -> CompiledStateGraph:
    if mock:
        from chatbot.agent.mock_agent import create_mock_graph

        agent = await create_mock_graph(checkpointer=checkpointer)
        return agent

    llm = await aget_model("gemini-flash-lite", temperature=0.0)
    tools = await get_tools(verbose)
    agent = await create_agent(llm, tools, name="default", checkpointer=checkpointer)
    return agent


async def get_agents_dict(
    checkpointer: BaseCheckpointSaver,
    verbose: bool = False,
    mock: bool = False,
) -> Dict[str, Pregel]:
    agents_dict = {}
    # Here you can define multiple agents with different configurations
    agent_names = ["default"]  # Extend this list as needed

    for name in agent_names:
        if mock:
            from chatbot.agent.mock_agent import create_mock_graph

            agents_dict[name] = await create_mock_graph(checkpointer=checkpointer)
        else:
            llm = await aget_model("gemini-flash-lite", temperature=0.0)
            tools = await get_tools(verbose)
            agents_dict[name] = await create_agent(
                llm,
                tools,
                name=name,
                checkpointer=checkpointer,
            )

    return agents_dict
