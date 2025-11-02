from pathlib import Path
from typing import List, cast

from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings

from chatbot.agent.answering import create_agent, get_tools
from chatbot.agent.models import AnsweringState
from chatbot.logging import HERE
from chatbot.utils import get_embedding_model, get_model
from chatbot.vector_store.vector_store import get_vector_store

HERE = Path(__file__).parent.resolve()

if __name__ == "__main__":
    path_vector_store: str = f"{HERE}/../resources/embedding_data/data.json"
    embedder: OllamaEmbeddings = get_embedding_model()
    vector_store: InMemoryVectorStore = get_vector_store(
        embedder, path=path_vector_store
    )

    llm = get_model(service="ollama", model_name="qwen3:8b", temperature=0.0)

    agent = create_agent(llm=llm, tools=get_tools(vector_store, k=5, verbose=True))

    query = "When is Paris Hilton birthday?"
    state: AnsweringState = AnsweringState(
        messages=[HumanMessage(content=query)],
        answer=None,
        documents=None,
        remaining_steps=5,
    )

    res_ = agent.invoke(state)
    res: AnsweringState = cast(AnsweringState, res_)
    print(res)

    for m in res["messages"]:
        m.pretty_print()
