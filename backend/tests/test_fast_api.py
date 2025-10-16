from langchain_core.messages import HumanMessage
from fastapi.testclient import TestClient
import asyncio

from chatbot.api.main import app



async def test_chat_endpoint(client: TestClient):
    thread_id = "test-thread"
    payload = {
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What is the capital of France?"}
                    ],
                }
            ],
            "answer": None,
            "remaining_steps": 3,
        }
    }

    response = client.post(f"/agent/chat/{thread_id}", json=payload)
    print(response.status_code)
    print(response)
    # for chunk in response.iter_text():
    #     print(chunk)


if __name__ == "__main__":
    with TestClient(app) as client:
        asyncio.run(test_chat_endpoint(client))
