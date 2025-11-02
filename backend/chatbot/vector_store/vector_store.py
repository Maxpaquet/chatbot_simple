from typing import Optional

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings


def get_vector_store(
    embedding_model: OllamaEmbeddings,
    path: Optional[str] = None,
) -> InMemoryVectorStore:
    """Initialize and return an in-memory vector store."""
    if path is None:
        return InMemoryVectorStore(embedding=embedding_model)
    vector_store = InMemoryVectorStore.load(path=path, embedding=embedding_model)
    return vector_store
