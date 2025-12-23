from pathlib import Path
from typing import Dict, List, Optional
from uuid import uuid4

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.pregel import Pregel
from typing_extensions import TypedDict

from chatbot import agent
from chatbot.agent.answering import AnsweringState, create_agent, get_tools
from chatbot.agent.main import get_agents_dict
from chatbot.config import config
from chatbot.services.utils import prep_config, prep_input
from chatbot.utils import get_model

HERE = Path(__file__).parent

CHECKPOINT_SQLITE = f"{HERE}/../data/checkpoint.db"


async def main():
    thread_id = str(uuid4())
    checkpointer = None
    # with SqliteSaver.from_conn_string(CHECKPOINT_SQLITE) as checkpointer:
    agents_dict: Dict[str, Pregel] = await get_agents_dict(
        checkpointer,
        store=None,
        k=5,
        verbose=config.verbose,
        mock=config.mock,
    )
    agent: Pregel = agents_dict["simple"]

    input_state = AnsweringState(
        messages=[HumanMessage(content="What is the capital of France?")],
        answer=None,
        documents=None,
        remaining_steps=10,
    )

    config_langchain: RunnableConfig = await prep_config(
        thread_id, config.langfuse_config
    )

    res = await agent.ainvoke(
        input_state,
        config=config_langchain,
    )
    # print(res)
    print("*" * 100)
    for m in res["messages"]:
        m.pretty_print()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
