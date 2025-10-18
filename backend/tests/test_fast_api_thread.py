from langchain_core.messages import HumanMessage
from fastapi.testclient import TestClient
import asyncio
from uuid import uuid4

from chatbot.messages.models import MessageOut, MessageIn, Author
from chatbot.services.models import ChatRequest, Thread

from chatbot.api.main import app


async def _thread_endpoint(client: TestClient):
    # First send something to be stored in the database
    thread_id = "test-" + str(uuid4())
    message: MessageIn = MessageIn(
        id=str(uuid4()),
        author=Author.user,
        content="What is the capital of France?",
    )
    chat_request = ChatRequest(
        thread_id=thread_id,
        input=message,
    )
    payload = chat_request.model_dump()

    response = client.post(f"/agent/chat/{thread_id}", json=payload)
    assert response.status_code == 200

    response = client.get(f"/agent/chat/thread/{thread_id}")
    print(response.status_code)
    assert response.status_code == 200

    thread: Thread = Thread.model_validate(response.json())
    assert thread.thread_id == thread_id
    assert len(thread.conversation) >= 3


def test_thread_endpoint():
    with TestClient(app) as client:
        asyncio.run(_thread_endpoint(client))


if __name__ == "__main__":
    test_thread_endpoint()
