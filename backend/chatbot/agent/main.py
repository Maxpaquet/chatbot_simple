from pathlib import Path
from typing import Dict, Optional, Union

from langchain_core.language_models import LanguageModelInput
from langchain_core.runnables import Runnable
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.pregel import Pregel
from langgraph.store.base import BaseStore
from pydantic import BaseModel

from chatbot.agent.answering import create_agent, get_tools
from chatbot.agent.models import Answer
from chatbot.utils import get_embedding_model, get_model
from chatbot.vector_store.vector_store import get_vector_store

HERE = Path(__file__).parent.resolve()


async def get_agent(
    llm: ChatOllama | ChatGoogleGenerativeAI,
    vector_store: InMemoryVectorStore,
    checkpointer: Optional[BaseCheckpointSaver],
    verbose: bool = False,
    mock: bool = False,
) -> CompiledStateGraph:
    if mock:
        from chatbot.agent.mock_agent import create_mock_graph

        agent = await create_mock_graph(checkpointer=checkpointer)
        return agent

    # llm: ChatOllama | ChatGoogleGenerativeAI = await aget_model("ollama", "qwen3:8b", temperature=0.0)
    llm_with_structured_output: Runnable[LanguageModelInput, Union[dict, BaseModel]] = (
        llm.with_structured_output(Answer)
    )
    tools = await get_tools(vector_store, llm_with_structured_output, verbose=verbose)
    agent = await create_agent(llm, tools, checkpointer=checkpointer)
    return agent


async def get_agents_dict(
    checkpointer: BaseCheckpointSaver,
    store: Optional[BaseStore] = None,
    verbose: bool = False,
    mock: bool = False,
) -> Dict[str, Pregel]:
    agents_dict = {}
    # Here you can define multiple agents with different configurations
    agent_names = ["default"]  # Extend this list as needed

    path_vector_store: str = f"{HERE}/../resources/embedding_data/data.json"
    embedder: OllamaEmbeddings = get_embedding_model()
    vector_store: InMemoryVectorStore = get_vector_store(
        embedder, path=path_vector_store
    )
    for name in agent_names:
        if mock:
            from chatbot.agent.mock_agent import create_mock_graph

            agents_dict[name] = await create_mock_graph(checkpointer=checkpointer)
        else:
            llm = get_model(service="ollama", model_name="qwen3:8b", temperature=0.0)
            llm_with_structured_output: Runnable[
                LanguageModelInput, Union[dict, BaseModel]
            ] = llm.with_structured_output(Answer)
            tools = await get_tools(vector_store, llm_with_structured_output, verbose)
            agents_dict[name] = await create_agent(
                llm,
                tools,
                store=store,
                checkpointer=checkpointer,
            )

    return agents_dict
