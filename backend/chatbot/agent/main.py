from pathlib import Path
from typing import Dict, Optional

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.pregel import Pregel
from langgraph.store.base import BaseStore

from chatbot.agent.answering import create_agent, get_tools
from chatbot.agent.models import Answer
from chatbot.agent.simple import create_simple_agent
from chatbot.config import LLMModelConfig, config
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

    llm_with_structured_output = llm.with_structured_output(Answer)
    tools = await get_tools(vector_store, llm_with_structured_output, verbose=verbose)
    agent = await create_agent(llm, tools, checkpointer=checkpointer)
    return agent


async def get_agents_dict(
    checkpointer: Optional[BaseCheckpointSaver],
    store: Optional[BaseStore] = None,
    k: int = 5,
    verbose: bool = False,
    mock: bool = False,
) -> Dict[str, Pregel]:
    agents_dict: Dict[str, Pregel] = {}

    # Load the LLM configuration from the global config
    # llm = get_model(service="ollama", model_name="qwen3:8b", temperature=0.0)
    config_llm: LLMModelConfig = config.llm.default()

    llm: ChatOllama | ChatGoogleGenerativeAI = get_model(
        service=config_llm.service,
        model_name=config_llm.model_name,
        temperature=config_llm.temperature,
        seed=config_llm.seed,
    )

    # Define a simple agent that is just a LLM
    agents_dict["simple"] = await create_simple_agent(llm, checkpointer, store)

    # Here you can define multiple agents with different configurations
    agent_names = ["default"]  # Extend this list as needed

    path_vector_store: str = f"{HERE}/../../resources/embedding_data/data.json"
    embedder: OllamaEmbeddings = get_embedding_model()
    vector_store: InMemoryVectorStore = get_vector_store(
        embedder, path=path_vector_store
    )
    for name in agent_names:
        if mock:
            from chatbot.agent.mock_agent import create_mock_graph

            agents_dict[name] = await create_mock_graph(checkpointer=checkpointer)
        else:
            llm_with_structured_output = llm.with_structured_output(Answer)
            tools = await get_tools(
                vector_store,
                llm_with_structured_output,
                k=k,
                verbose=verbose,
            )
            agents_dict[name] = await create_agent(
                llm,
                tools,
                store=store,
                checkpointer=checkpointer,
            )

    return agents_dict
