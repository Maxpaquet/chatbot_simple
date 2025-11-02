import sys
from typing import Annotated, Callable, List, Literal, Optional, TypedDict

from langchain_core.documents import Document
from langchain_core.language_models import (
    BaseChatModel,
    BaseLanguageModel,
    LanguageModelInput,
)
from langchain_core.messages import (
    AnyMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool, tool
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.vectorstores import VectorStore
from langchain_ollama import ChatOllama
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import InjectedState, ToolNode, create_react_agent
from langgraph.store.base import BaseStore
from langgraph.types import Command

from chatbot.agent.models import Answer, AnsweringState
from chatbot.agent.utils import MAX_CHAR, documents_to_str

SYSTEM_PROMPT = (
    """You are an AI assistant that helps people answering their question."""
)


def get_tools(
    vector_store: VectorStore,
    k: int = 5,
    verbose: bool = False,
) -> List[BaseTool]:
    @tool
    def answer(
        reasoning: Annotated[
            str, "The reasoning behind choosing this tool with the argument"
        ],
        final_answer: Annotated[str, "The final answer to the question of the user"],
        state: Annotated[AnsweringState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ):
        """Use this function to formulate the final answer when you have all the documentation to answer. Once you use this tool, the agent will stop."""
        if verbose:
            print(
                f"[formulate_answer] final_answer={str(final_answer)}\nreasoning: {reasoning}"
            )
        return Command(
            update={
                "answer": final_answer,
                "messages": [
                    ToolMessage(
                        content=str(final_answer),
                        artifact=final_answer,
                        tool_call_id=tool_call_id,
                    )
                ],
            }
        )

    @tool
    def search(
        reasoning: Annotated[
            str, "The reasoning behind choosing this tool with the argument"
        ],
        queries: Annotated[List[str], "The list of queries to search in the database."],
        state: Annotated[AnsweringState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ):
        """Use this function to search information in the vector database."""
        if verbose:
            print(f"[search] queries={queries}\nreasoning: {reasoning}")

        # Perform similarity search for each query and aggregate results
        all_results: List[tuple[Document, float]] = [
            (doc, score)
            for query in queries
            for doc, score in vector_store.similarity_search_with_score(query, k=k)
        ]

        # Remove duplicate documents by id (if available), else by content hash
        seen = set()
        documents: List[Document] = []
        for doc, _ in all_results:
            doc_id = doc.metadata.get("id", None)
            if doc_id not in seen:
                seen.add(doc_id)
            documents.append(doc)

        doc_str: str = "\n\n".join([documents_to_str(doc) for doc in documents])[
            :MAX_CHAR
        ]
        return Command(
            update={
                "messages": [
                    ToolMessage(
                        content="The retrieved documents are:\n" + doc_str,
                        artifact=documents,
                        tool_call_id=tool_call_id,
                    )
                ],
                "documents": (state.get("documents") or []) + documents,
            }
        )

    return [answer, search]


def choose_tools_node(
    llm_with_tools: Runnable[LanguageModelInput, BaseMessage],
    system_prompt: str = SYSTEM_PROMPT,
) -> Callable:

    def process(state: AnsweringState):
        # messages = ChatPromptTemplate.from_messages([
        #     ("system", system_prompt),
        #     MessagesPlaceholder(variable_name="messages"),
        # ])
        messages: List[AnyMessage] = [SystemMessage(content=system_prompt)] + state.get(
            "messages", []
        )

        for m in messages:
            m.pretty_print()

        response = llm_with_tools.invoke(input=messages)
        print(f"[choose_tools_node] Response from choose_tools_node: {response}")
        return {"messages": response}

    return process


def should_continue(state: AnsweringState):
    for m in state["messages"]:
        m.pretty_print()
    # Find the latest ToolMessage in reverse order
    last_tool_message = next(
        (m for m in reversed(state["messages"]) if isinstance(m, ToolMessage)), None
    )
    assert last_tool_message is not None, "No ToolMessage found in messages."
    if last_tool_message.name == "formulate_answer":
        print(f"[should_continue] Ending workflow.")
        return END
    print(f"[should_continue] Continuing to choose tools.")
    return "choose_tools"


def create_agent(
    llm: BaseChatModel,
    tools: List[BaseTool],
    store: Optional[BaseStore] = None,
    checkpointer: Optional[BaseCheckpointSaver] = None,
) -> CompiledStateGraph:
    llm_with_tools: Runnable[LanguageModelInput, BaseMessage] = llm.bind_tools(tools)

    node_choose_tools: Callable = choose_tools_node(llm_with_tools)
    tool_node = ToolNode(tools, handle_tool_errors=False)

    workflow = StateGraph(AnsweringState)
    workflow.add_node("choose_tools", node_choose_tools)
    workflow.add_node("tools", tool_node)
    workflow.add_edge("choose_tools", "tools")
    workflow.add_conditional_edges("tools", should_continue)
    workflow.set_entry_point("choose_tools")

    app: CompiledStateGraph = workflow.compile(checkpointer=checkpointer, store=store)
    return app


# async def create_agent(
#     model: BaseLanguageModel,
#     tools: List[BaseTool],
#     name: str,
#     store: Optional[BaseStore] = None,
#     checkpointer: Optional[BaseCheckpointSaver] = None,
# ) -> CompiledStateGraph:
#     """
#     Creates and configures a ReAct agent with the specified language model, tools, and optional storage and checkpointing.

#     Args:
#         model (BaseLanguageModel): The language model to be used by the agent.
#         tools (List[BaseTool]): A list of tools that the agent can utilize.
#         store (Optional[BaseStore], optional): An optional storage backend for the agent's state. Defaults to None.
#         checkpointer (Optional[BaseCheckpointSaver], optional): An optional checkpoint saver for persisting agent state. Defaults to None.

#     Returns:
#         CompiledStateGraph: The initialized and compiled agent ready for use.
#     """
#     kwargs = {
#         "model": model,
#         "tools": tools,
#         "state_schema": AnsweringState,
#         "prompt": SYSTEM_PROMPT,
#         "name": name,
#     }
#     if store is not None:
#         kwargs["store"] = store
#     if checkpointer is not None:
#         kwargs["checkpointer"] = checkpointer

#     return create_react_agent(**kwargs)
