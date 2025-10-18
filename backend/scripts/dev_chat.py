from langchain_core.messages import HumanMessage
from fastapi.testclient import TestClient
from httpx import AsyncClient
from uuid import uuid4

from chatbot.messages.models import MessageIn, Author
from chatbot.services.models import ChatRequest

from chatbot.api.main import app
import asyncio


async def test_chat_endpoint(client: TestClient):
    thread_id = "test-" + str(uuid4())
    message: MessageIn = MessageIn(
        id=str(uuid4()),
        author=Author.user,
        content="What is the capital of France?",
    )
    chat_request = ChatRequest(
        thread_id=thread_id,
        input=message,
        agent_id=None,
    )
    payload = chat_request.model_dump()

    response = client.post(f"/agent/chat/{thread_id}", json=payload)
    print(response.status_code)
    print(response.content)


# async def main():


if __name__ == "__main__":
    with TestClient(app) as client:
        asyncio.run(test_chat_endpoint(client))
