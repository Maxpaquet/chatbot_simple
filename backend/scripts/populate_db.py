from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings

from chatbot.utils import get_embedding_model
from chatbot.vector_store.chunker import (
    load_pdf_text_plumber,
    populate_db,
    split_text,
    texts_to_documents,
)
from chatbot.vector_store.vector_store import get_vector_store

HERE = Path(__file__).parent.resolve()

if __name__ == "__main__":
    folder_path = f"{HERE}/../resources/embedding_data"
    pdf_paths = [
        f"{folder_path}/flower.pdf",
        f"{folder_path}/grande_depression.pdf",
        f"{folder_path}/paris_hilton.pdf",
    ]

    embedder: OllamaEmbeddings = get_embedding_model()
    vector_store: InMemoryVectorStore = get_vector_store(embedder)

    all_docs: List[Document] = []
    for path in pdf_paths:
        # Load and process PDF
        text: str = load_pdf_text_plumber(path)
        chunks: List[str] = split_text([text])
        filename_str: str = Path(path).stem
        docs: List[Document] = texts_to_documents(chunks, filename_str)
        all_docs.extend(docs)

    ids = populate_db(vector_store, all_docs)
    print(f"Added document IDs: {len(ids)}")

    vector_store.dump(f"{folder_path}/data.json")
