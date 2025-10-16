from langchain_core.messages import HumanMessage, SystemMessage

from chatbot.agent.main import get_agent
from chatbot.agent.models import AnsweringState

if __name__ == "__main__":
    agent = get_agent(checkpointer=None, mock=True)
    print("Mock agent created successfully.")

    state = AnsweringState(
        messages=[
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="Human message mock"),
        ],
        answer=None,
        remaining_steps=10,
    )

    final_state = agent.invoke(state)
    print("Final state after running the mock agent:")
    # print(final_state)
    for m in final_state["messages"]:
        m.pretty_print()
