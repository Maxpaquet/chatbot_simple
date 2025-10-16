from langchain_core.messages import HumanMessage
from fastapi.testclient import TestClient
from httpx import AsyncClient

from chatbot.api.main import app
import asyncio


async def test_chat_endpoint(cient: AsyncClient):
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

    async with cient.stream("POST", f"/agent/chat/{thread_id}", json=payload) as stream:
        a = stream
        # async for chunk in stream.aiter_text():
        #     print("*" * 20)
        #     print(chunk)


async def main():
    headers = {"User-Agent": "test-client"}
    async with AsyncClient(base_url="http://localhost:8000", headers=headers) as client:
        await test_chat_endpoint(client)


if __name__ == "__main__":
    asyncio.run(main())
