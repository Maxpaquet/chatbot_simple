from typing import Literal
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

MODEL_MAP = {
    "gemini": "gemini-2.5-flash",
    "gemini-pro": "gemini-2.5-pro",
    "gemini-flash-lite": "gemini-2.5-flash-lite",
}

def _create_model(model_name: str, temperature: float):
    model_key = MODEL_MAP.get(model_name)
    if not model_key:
        raise ValueError(
            f"Unknown model name: {model_name}. Supported: {', '.join(MODEL_MAP.keys())}."
        )
    return ChatGoogleGenerativeAI(
        model=model_key,
        temperature=temperature,
        max_retries=2,
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )

async def aget_model(
    model_name: Literal["gemini", "gemini-pro", "gemini-flash-lite"] = "gemini-flash-lite",
    temperature=0.0,
):
    return _create_model(model_name, temperature)

def get_model(
    model_name: Literal["gemini", "gemini-pro", "gemini-flash-lite"] = "gemini-flash-lite",
    temperature=0.0,
):
    return _create_model(model_name, temperature)
