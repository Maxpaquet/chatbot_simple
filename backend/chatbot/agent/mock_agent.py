from typing import Annotated, Optional, List
from typing_extensions import TypedDict


from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages, AnyMessage
from langgraph.prebuilt import InjectedState, ToolNode
from langgraph.types import Command
from langgraph.checkpoint.base import BaseCheckpointSaver

from langchain_core.messages import AIMessage, ToolMessage, SystemMessage
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.tools import BaseTool, tool


# Define Answer and AnsweringState as in answering.py
class AnswerMock(TypedDict):
    item: str


class AnsweringStateMock(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    answer: Optional[AnswerMock]
    remaining_steps: int


# # Define a mock tool
# @tool
# def mock_tool(
#     reasoning: Annotated[str, "Reasoning for using the tool"],
#     final_answer: Annotated[AnswerMock, "The final answer to the question of the user"],
#     state: Annotated[AnsweringStateMock, InjectedState],
#     tool_call_id: Annotated[str, InjectedToolCallId],
# ):
#     """Mock tool that simulates answering a question."""
#     return Command(
#         update={
#             "answer": final_answer,
#             "messages": [
#                 ToolMessage(
#                     content=str(final_answer),
#                     artifact=final_answer,
#                     tool_call_id=tool_call_id,
#                 )
#             ],
#         }
#     )


# tools: List[BaseTool] = [mock_tool]


# # The agent node returns an AIMessage with a tool call (tool_call_id must match what ToolNode expects)
# def mock_agent_node(state: AnsweringStateMock) -> Command:
#     ai_msg = AIMessage(
#         content="This is a mock AI response. [mock_tool will be called]",
#         tool_calls=[
#             {
#                 "name": "mock_tool",
#                 "args": {
#                     "reasoning": "Mock reasoning",
#                     "final_answer": {"item": "Mocked tool answer"},
#                 },
#                 "id": "mock_tool_call_id",
#             }
#         ],
#     )
#     # return Command(
#     #     update={
#     #         "messages": [ai_msg],
#     #         "remaining_steps": state.get("remaining_steps", 2) - 1,
#     #     }
#     # )
#     # After the agent node, set remaining_steps to 1 so ToolNode runs once, then graph ends
#     return Command(
#         update={
#             "messages": [ai_msg],
#             "remaining_steps": 0,  # End after ToolNode
#             "answer": state.get("answer", None),
#         }
#     )


def create_mock_graph(
    checkpointer: Optional[BaseCheckpointSaver] = None,
):

    def mock_agent_node(state: AnsweringStateMock):
        # system_message = SystemMessage(content = "You are a helpful assistant.")
        print("[mock_agent_node]")
        return {"messages": AIMessage(content="This is a mock AI response.")}

    def mock_tool_node(state: AnsweringStateMock):
        print("[mock_tool_node]")
        return {
            "messages": ToolMessage(
                content="This is a mock Tool response.",
                tool_call_id="mock_tool_call_id",
            )
        }

    graph = StateGraph(state_schema=AnsweringStateMock)
    graph.add_node("agent", mock_agent_node)
    graph.add_node("tool", mock_tool_node)

    graph.add_edge("agent", "tool")

    graph.set_entry_point("agent")
    graph.set_finish_point("tool")

    if checkpointer is not None:
        return graph.compile(checkpointer=checkpointer)
    else:
        return graph.compile()
