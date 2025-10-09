from langgraph.store.base import BaseStore
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph

from chatbot.agent.answering import create_agent, get_tools
from chatbot.utils import get_model


def get_agent(
    checkpointer: BaseCheckpointSaver,
    verbose: bool = False,
) -> CompiledStateGraph:

    llm = get_model("gemini-flash-lite", temperature=0.0)
    tools = get_tools(verbose)
    agent = create_agent(llm, tools, checkpointer=checkpointer)
    return agent
