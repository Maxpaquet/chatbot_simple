from typing import List
from chatbot.utils import get_embedding_model
from langchain_ollama import OllamaEmbeddings

def main(embeddings: OllamaEmbeddings, texts: List[str]):
    vectors = embeddings.embed_documents(texts)
    for i, vector in enumerate(vectors):
        print(f"Text: {texts[i]}\nVector: {vector}\n")


if __name__ == "__main__":
    embedding_model = get_embedding_model()
    sample_texts = [
        "Hello, how are you?",
        "What is the capital of France?",
        "Explain the theory of relativity."
    ]
    main(embedding_model, sample_texts)