from typing import List
from uuid import uuid4

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import pdfplumber


def load_pdf_text_plumber(file_path) -> str:
    """Load text from a PDF file using pdfplumber."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


def split_text(
    texts: List[str], chunk_size: int = 500, chunk_overlap: int = 50
) -> List[str]:
    """Split texts into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return [chunk for text in texts for chunk in text_splitter.split_text(text)]


def texts_to_documents(texts: List[str], document_name: str) -> List[Document]:
    """Convert texts to Document objects with metadata."""
    docs: List[Document] = []
    for k, text in enumerate(texts):
        docs.append(
            Document(
                page_content=text,
                metadata={
                    "filename": document_name,
                    "chunk": k,
                    "id": str(uuid4()),
                },
            )
        )
    return docs


def populate_db(
    vector_store: InMemoryVectorStore, documents: List[Document]
) -> List[str]:
    """Add documents to the vector store and return their IDs."""
    ids: List[str] = vector_store.add_documents(documents)
    return ids
