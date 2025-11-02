from typing import Literal
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama, OllamaEmbeddings
from dotenv import load_dotenv

load_dotenv()

MODEL_MAP_GEMINI = {
    "gemini": "gemini-2.5-flash",
    "gemini-pro": "gemini-2.5-pro",
    "gemini-flash-lite": "gemini-2.5-flash-lite",
}

MODEL_LIST_OLLAMA = ["qwen3:8b"]
MODEL_LIST_EMBEDDINGS = ["qwen3-embedding:0.6b"]


def _create_model_gemini(model_name: str, temperature: float) -> ChatGoogleGenerativeAI:
    model_key = MODEL_MAP_GEMINI.get(model_name)
    if not model_key:
        raise ValueError(
            f"Unknown model name: {model_name}. Supported: {', '.join(MODEL_MAP_GEMINI.keys())}."
        )
    return ChatGoogleGenerativeAI(
        model=model_key,
        temperature=temperature,
        max_retries=2,
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )


def _create_model_ollama(model_name: str, temperature: float) -> ChatOllama:
    if model_name not in MODEL_LIST_OLLAMA:
        raise ValueError(
            f"Unknown model name: {model_name}. Supported: {', '.join(MODEL_LIST_OLLAMA)}."
        )
    return ChatOllama(
        model=model_name,
        temperature=temperature,
        validate_model_on_init=True,
    )


async def aget_model(
    service: Literal["gemini", "ollama"] = "ollama",
    model_name: Literal[
        "gemini", "gemini-pro", "gemini-flash-lite"
    ] = "gemini-flash-lite",
    temperature=0.0,
):
    if service == "ollama":
        return _create_model_ollama(model_name, temperature)
    elif service == "gemini":
        return _create_model_gemini(model_name, temperature)
    else:
        raise ValueError(f"Unknown service: {service}. Supported: gemini, ollama.")


def get_model(
    model_name: Literal[
        "gemini", "gemini-pro", "gemini-flash-lite"
    ] = "gemini-flash-lite",
    temperature=0.0,
):
    return _create_model_gemini(model_name, temperature)


def _create_embedding_model_ollama(model_name: str) -> OllamaEmbeddings:
    if model_name not in MODEL_LIST_EMBEDDINGS:
        raise ValueError(
            f"Unknown embedding model name: {model_name}. Supported: {', '.join(MODEL_LIST_EMBEDDINGS)}."
        )
    return OllamaEmbeddings(model=model_name)


def get_embedding_model(
    serive: Literal["ollama"] = "ollama",
    model_name: Literal["qwen3-embedding:0.6b"] = "qwen3-embedding:0.6b",
):
    if serive == "ollama":
        return _create_embedding_model_ollama(model_name)
    else:
        raise ValueError(f"Unknown service: {serive}. Supported: ollama.")
