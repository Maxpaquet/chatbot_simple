from typing import Optional

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import StateGraph
from langgraph.store.base import BaseStore

from chatbot.agent.models import AnsweringState

SYSTEM_PROMPT_SIMPLE = (
    """You are an AI assistant that helps people answering their question."""
)


async def process_simple_agent(
    llm: ChatOllama | ChatGoogleGenerativeAI,
    system_prompt: str = SYSTEM_PROMPT_SIMPLE,
):
    """
    Creates a processing function that invokes the LLM with a system prompt and message history.
    """

    def process(state: AnsweringState):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("messages"),
            ]
        )
        res = (prompt | llm).invoke(input=dict(state))
        return {"messages": res}

    return process


async def create_simple_agent(
    llm: ChatOllama | ChatGoogleGenerativeAI,
    checkpointer: Optional[BaseCheckpointSaver] = None,
    store: Optional[BaseStore] = None,
):
    """
    Creates and compiles a state graph for a simple chatbot agent.
    Initializes a single-node graph using the provided LLM, setting it as both entry and finish point.
    Compiles the graph with optional checkpointer and store.
    """
    workflow = StateGraph(AnsweringState)
    simple_node_ = await process_simple_agent(llm)
    workflow.add_node("simple_node", simple_node_)

    workflow.set_entry_point("simple_node")
    workflow.set_finish_point("simple_node")

    compiled_graph = workflow.compile(checkpointer=checkpointer, store=store)

    return compiled_graph
