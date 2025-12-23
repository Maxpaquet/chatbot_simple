from typing import Annotated, Callable, Dict, List, Optional, Union

from langchain_core.documents import Document
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    ToolMessage,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool, tool
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.vectorstores import VectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import InjectedState, ToolNode
from langgraph.store.base import BaseStore
from langgraph.types import Command
from pydantic import BaseModel

from chatbot.agent.models import Answer, AnsweringState
from chatbot.agent.utils import MAX_CHAR, documents_to_str
from chatbot.logging import logger

SYSTEM_PROMPT = (
    """You are an AI assistant that helps people answering their question."""
)


async def get_tools(
    vector_store: VectorStore,
    llm_structured_output: Runnable[LanguageModelInput, Union[Dict, BaseModel]],
    k: int = 5,
    verbose: bool = False,
) -> List[BaseTool]:

    @tool
    async def answer(
        reasoning: Annotated[
            str, "The reasoning behind choosing this tool with the argument"
        ],
        state: Annotated[AnsweringState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ):
        """Use this function to formulate the final answer when you have all the documentation to answer. Once you use this tool, the agent will stop."""
        if verbose:
            print(f"[formulate_answer] reasoning: {reasoning}")
        result = await llm_structured_output.ainvoke(input=state["messages"])
        # if isinstance(result, Answer):
        #     final_answer = result
        # elif isinstance(result, dict):
        #     final_answer = Answer(**result)
        # else:
        #     logger.error(f"Unexpected type for final_answer: {type(result)}")
        #     final_answer = result
        #     # raise TypeError(f"Unexpected type for final_answer: {type(result)}")
        if isinstance(result, BaseMessage):
            final_answer = result.content
        else:
            final_answer = result
        if verbose:
            logger.info(f"[formulate_answer] final_answer:\n{str(final_answer)}")
        return Command(
            update={
                # "answer": final_answer,
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
    async def search(
        reasoning: Annotated[
            str, "The reasoning behind choosing this tool with the argument"
        ],
        queries: Annotated[List[str], "The list of queries to search in the database."],
        state: Annotated[AnsweringState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ):
        """Use this function to search information in the vector database."""
        if verbose:
            logger.info(f"[search] queries={queries}\nreasoning: {reasoning}")

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

    return [answer]  # , search


def choose_tools_node(
    llm_with_tools: Runnable[LanguageModelInput, BaseMessage],
    system_prompt: str = SYSTEM_PROMPT,
) -> Callable:

    def process(state: AnsweringState):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("messages"),
            ]
        )

        response = (prompt | llm_with_tools).invoke(input=dict(state))
        logger.info(
            f"[choose_tools_node] Response from choose_tools_node: {response.content}"
        )
        return {"messages": response}

    return process


def should_continue(state: AnsweringState):
    last_message: BaseMessage = state["messages"][-1]
    logger.info(f"[should_continue] Last message type: {type(last_message)}")
    logger.info(f"[should_continue] Last message content: {last_message.content}")
    if isinstance(last_message, AIMessage):
        return END
    if isinstance(last_message, ToolMessage):
        logger.info(f"[should_continue] Last tool message name: {last_message.name}")
        if last_message.name == "answer":
            logger.info(f"[should_continue] Ending workflow.")
            return END
    logger.info(f"[should_continue] Continuing to choose tools.")
    return "choose_tools"


async def create_agent(
    llm: ChatOllama | ChatGoogleGenerativeAI,
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
