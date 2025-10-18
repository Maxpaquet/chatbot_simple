from langchain_core.messages import HumanMessage
from fastapi.testclient import TestClient
import asyncio
from uuid import uuid4

from chatbot.messages.models import MessageIn, Author
from chatbot.services.models import ChatRequest
from chatbot.api.main import app


async def _chat_endpoint(client: TestClient):
    thread_id = "test-thread"
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
    assert response.status_code == 200
    print(response.status_code)
    print(response)
    # for chunk in response.iter_text():
    #     print(chunk)


def test_chat_endpoint():
    with TestClient(app) as client:
        asyncio.run(_chat_endpoint(client))
