from typing import List, Optional
from typing_extensions import TypedDict
from pathlib import Path
from uuid import uuid4

from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage, BaseMessage, SystemMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.runnables import RunnableConfig

from chatbot.agent.answering import create_agent, get_tools, AnsweringState
from chatbot.utils import get_model
from chatbot.api.utils import prep_input

HERE = Path(__file__).parent

CHECKPOINT_SQLITE = f"{HERE}/../data/checkpoint.db"

if __name__ == "__main__":
    llm = get_model("gemini-flash-lite", temperature=0.0)
    tools: List[BaseTool] = get_tools(verbose=True)

    thread_id = str(uuid4())
    user_id = "user_1"
    config = RunnableConfig(configurable={"thread_id": thread_id, "user_id": user_id})

    with SqliteSaver.from_conn_string(CHECKPOINT_SQLITE) as checkpointer:
        agent = create_agent(
            llm,
            tools,
            store=None,
            checkpointer=checkpointer,
        )

        messages: List[BaseMessage] = [
            SystemMessage(
                content="You are a helpful assistant that helps people find information."
            ),
            HumanMessage(content="What is the capital of France?"),
        ]
        state_1 = AnsweringState(
            messages=messages,
            answer=None,
            remaining_steps=10,
        )
        res = agent.invoke(state_1, config=config)

        print(res)
        for m in res["messages"]:
            m.pretty_print()

        state_2 = AnsweringState(
            messages=[
                HumanMessage(
                    content="Repeat the name of the city and tell me what can I do in this city ?"
                )
            ],
            answer=None,
            remaining_steps=10,
        )

        res = agent.invoke(state_2, config=config)
        print("*" * 100)
        print(res)
        for m in res["messages"]:
            m.pretty_print()
