from typing import Literal
import os
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

load_dotenv()


async def get_model(
    model_name: Literal[
        "gemini-flash", "gemini-pro", "gemini-flash-lite"
    ] = "gemini-flash-lite",
    temperature=0.0,
):
    if model_name == "gemini":
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=temperature,
            max_retries=2,
            google_api_key=os.getenv("GEMINI_API_KEY"),
            # google_api_key=os.getenv("GOOGLE_API_KEY_MAX"),
        )
    elif model_name == "gemini-pro":
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=temperature,
            max_retries=2,
            google_api_key=os.getenv("GEMINI_API_KEY"),
            # google_api_key=os.getenv("GOOGLE_API_KEY_MAX"),
        )
    elif model_name == "gemini-flash-lite":
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=temperature,
            max_retries=2,
            google_api_key=os.getenv("GEMINI_API_KEY"),
            # google_api_key=os.getenv("GOOGLE_API_KEY_MAX"),
        )
    else:
        raise ValueError(
            f"Unknown model name: {model_name}. Supported: gemini, gemini-pro, claude."
        )


