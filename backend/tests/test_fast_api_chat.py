import asyncio
from uuid import uuid4

from fastapi.testclient import TestClient

from chatbot.api.main import app
from chatbot.messages.models import Author, MessageIn
from chatbot.services.models import ChatRequest, Thread


async def _chat_endpoint(client: TestClient):
    # thread_id = "test-thread"
    thread_id = "test-123456"
    # thread_id = str(uuid4())
    message: MessageIn = MessageIn(
        id=str(uuid4()),
        author=Author.user,
        content="What is the capital of France?",
    )
    chat_request = ChatRequest(
        thread_id=thread_id,
        input=message,
        agent_id="simple",
    )
    payload = chat_request.model_dump()

    response = client.post(f"/agent/chat/{thread_id}", json=payload)
    assert response.status_code == 200
    print(response.status_code)
    print(response.content)
    # for chunk in response.iter_text():
    #     print(chunk)

    response = client.get(f"/agent/chat/thread/{thread_id}")
    print(response.content)

    thread: Thread = Thread.model_validate(response.json())
    print(thread)
    # assert thread.thread_id == thread_id


def test_chat_endpoint():
    with TestClient(app) as client:
        asyncio.run(_chat_endpoint(client))


if __name__ == "__main__":
    test_chat_endpoint()
