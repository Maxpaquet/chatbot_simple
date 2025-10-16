from langgraph.store.base import BaseStore
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph

from chatbot.agent.answering import create_agent, get_tools
from chatbot.utils import get_model


def get_agent(
    checkpointer: BaseCheckpointSaver,
    verbose: bool = False,
    mock: bool = False,
) -> CompiledStateGraph:
    if mock:
        from chatbot.agent.mock_agent import create_mock_graph

        agent = create_mock_graph(checkpointer=checkpointer)
        return agent

    llm = get_model("gemini-flash-lite", temperature=0.0)
    tools = get_tools(verbose)
    agent = create_agent(llm, tools, checkpointer=checkpointer)
    return agent
