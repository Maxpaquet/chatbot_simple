import asyncio
from enum import StrEnum
from typing import Annotated, List, Literal
from unittest.mock import Base

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import BaseTool, tool
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

# answer: Annotated[str, "The capital of the country"],


class TAGS(StrEnum):
    BUILDING = "building"
    PERSON = "person"


class Answer(BaseModel):
    tags: List[TAGS] = Field(..., description="The tags associated with the answer")


@tool
def get_capital(
    capital: Annotated[str, "The capital"],
) -> str:
    """Give the capital of the country"""
    return capital


@tool
def calculator(
    a: Annotated[float, "The first number"],
    b: Annotated[float, "the second number"],
    operation: Annotated[
        Literal["add", "subtract"], "The mathematical operation to perform"
    ],
) -> float:
    """Simulate a calculator tool."""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    else:
        return 0.0


async def main():
    llm = ChatOllama(
        model="qwen3:8b",
        validate_model_on_init=True,
        temperature=0.1,
    ).bind_tools([get_capital, calculator])

    system_message = SystemMessage(
        content="You are a helpful assistant. Select the appropriate tool to answer the user's question. You have access to the following tools: get_capital, calculator."
    )
    # message = HumanMessage(content=f"What is the capital of Westeros ?")
    message = HumanMessage(content=f"2+2 ?")
    messages = [system_message, message]
    res = await llm.ainvoke(messages)

    print(res)
    print(type(res))


if __name__ == "__main__":
    asyncio.run(main())
