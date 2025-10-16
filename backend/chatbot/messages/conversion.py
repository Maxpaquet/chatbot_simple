from typing import Any, Dict, List
from uuid import uuid4
from datetime import date

from langchain_core.messages import BaseMessage

from chatbot.messages.models import MessageIn, MessageOut, Author
from chatbot.services.models import Thread, ThreadID


async def conversion_from_langchain(thread_id: ThreadID, data: Dict[str, Any]) -> Any:
    messages: List[BaseMessage] = data.get("messages", [])
    messages_thred = []
    for m in messages:
        id_message: str = m.id if m.id is not None else str(uuid4())
        if isinstance(m.content, str):
            content: str = m.content
        elif isinstance(m.content, List):
            content: str = " ".join(str(item) for item in m.content)
        else:
            raise TypeError(
                f"[conversion_from_langchain] Unsupported content type: {type(m.content)}"
            )

        author_message: str = m.type
        match author_message:
            case "human":
                author = Author.user
            case "ai":
                author = Author.agent
            case "system":
                author = Author.system
            case "tool":
                author = Author.tool
            case _:
                raise ValueError(
                    f"[conversion_from_langchain] Unknown message type: {author_message}"
                )
        timestamp: date = date.today()
        messages_thred.append(
            MessageOut(
                author=author,
                content=content,
                id=id_message,
                timestamp=timestamp,
            )
        )
    return Thread(thread_id=thread_id, conversation=messages_thred)
