from langchain_core.documents import Document

MAX_CHAR = 2500

def documents_to_str(document: Document) -> str:
    """Convert a list of Document objects to a single string."""
    return f"Document: {document.metadata.get('filename', 'Unknown')}\nContent: {document.page_content}..."
