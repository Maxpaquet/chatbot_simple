from typing import Annotated, Optional, List, Callable, Dict, Any
from typing_extensions import TypedDict
from uuid import uuid4
import time

from langgraph.graph import StateGraph
from langgraph.types import Command
from langgraph.checkpoint.base import BaseCheckpointSaver

from langchain_core.tools import BaseTool, tool
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.messages.tool import ToolCall

from chatbot.agent.models import AnsweringState, Answer


def get_mock_tools() -> List[BaseTool]:
    @tool
    def mock_tool(
        reasoning: Annotated[str, "Reasoning for using the tool"],
        final_answer: Annotated[Answer, "The final answer to the question of the user"],
    ):
        """Mock tool that simulates answering a question."""
        return f"Processed: reasoning={reasoning}, final_answer={final_answer}"

    return [mock_tool]


def tool_choice_node() -> Callable:
    def process(state: AnsweringState) -> Command:
        tool_call_id: str = str(uuid4())
        tool_call = ToolCall(
            name="mock_tool",
            args={
                "reasoning": "Mock reasoning",
                "final_answer": {"item": "Mocked tool answer"},
            },
            id=tool_call_id,
        )
        ai_msg = AIMessage(
            content="This is a mock AI response. [mock_tool will be called]",
            tool_calls=[tool_call],
        )
        return Command(
            update={
                "messages": [ai_msg],
                "remaining_steps": 1,  # Let ToolNode run once
            }
        )

    return process


def tool_executer(state: AnsweringState) -> Dict:
    last_message = state["messages"][-1]
    assert isinstance(last_message, AIMessage)

    tool_call: ToolCall = last_message.tool_calls[0]
    tool_name: str = tool_call.get("name", "mock_tool")
    tool_args: Dict[str, Any] = tool_call.get("args", {"key": None})

    tool_call_id_value = tool_call.get("id")
    tool_call_id: str = (
        tool_call_id_value if tool_call_id_value is not None else str(uuid4())
    )

    tools: List[BaseTool] = get_mock_tools()

    print(f"tool_args: {tool_args}")

    tool = next((t for t in tools if t.name == tool_name), None)
    if tool is None:
        raise ValueError(f"Tool {tool_name} not found")

    result = tool.invoke(input=tool_args)
    time.sleep(1)
    return {"messages": ToolMessage(content=str(result), tool_call_id=tool_call_id)}


async def create_mock_graph(
    checkpointer: Optional[BaseCheckpointSaver] = None,
):
    graph = StateGraph(state_schema=AnsweringState)

    tool_choice_node_: Callable = tool_choice_node()

    graph.add_node("tool_choice", tool_choice_node_)
    graph.add_node("tool_executer", tool_executer)

    graph.add_edge("tool_choice", "tool_executer")

    graph.set_entry_point("tool_choice")
    graph.set_finish_point("tool_executer")

    if checkpointer is not None:
        return graph.compile(checkpointer=checkpointer)
    else:
        return graph.compile()
