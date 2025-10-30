from langchain_ollama import ChatOllama
from langchain_core.tools import tool, BaseTool

from langchain_core.messages import (
    AnyMessage,
    BaseMessage,
    ToolMessage,
    HumanMessage,
    SystemMessage,
)
from typing import Literal, Annotated, List, TypedDict, Callable
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from langchain_core.runnables import Runnable
from langgraph.prebuilt import ToolNode

from langchain_core.language_models import LanguageModelInput

llm = ChatOllama(
    model="qwen3:8b",
    validate_model_on_init=True,
    temperature=0.8,
)


class State(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    remaining_steps: int


@tool
def formulate_answer(
    answer: Annotated[str, "The final answer to give to the user"],
) -> str:
    """Formulate the final answer when you are ready."""
    return f"Search results for: {answer}"


@tool
def calculator(
    a: Annotated[float, "The first number"],
    b: Annotated[float, "the second number"],
    operation: Annotated[
        Literal["add", "subtract"], "The mathematical operation to perform"
    ],
) -> float:
    """Simulate a calculator tool."""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    else:
        return 0.0


def choose_tools_node(
    llm_with_tools: Runnable[LanguageModelInput, BaseMessage],
) -> Callable:

    def process(state: State):
        response = llm_with_tools.invoke(input=state["messages"])
        print(f"[choose_tools_node] Response from choose_tools_node: {response}")
        return {"messages": response}

    return process


def should_continue(state: State):
    last_message = state["messages"][-1]
    assert isinstance(last_message, ToolMessage)
    if last_message.name == "formulate_answer":
        print(f"[should_continue] Ending workflow.")
        return END
    print(f"[should_continue] Continuing to choose tools.")
    return "choose_tools"


def get_graph(llm: ChatOllama, tools: List[BaseTool]):
    llm_with_tools: Runnable[LanguageModelInput, BaseMessage] = llm.bind_tools(tools)

    node_choose_tools: Callable = choose_tools_node(llm_with_tools)
    tool_node = ToolNode(tools, handle_tool_errors=False)

    workflow = StateGraph(State)
    workflow.add_node("choose_tools", node_choose_tools)
    workflow.add_node("tools", tool_node)
    workflow.add_edge("choose_tools", "tools")
    workflow.add_conditional_edges("tools", should_continue)
    workflow.set_entry_point("choose_tools")

    app: CompiledStateGraph = workflow.compile()
    return app


if __name__ == "__main__":
    tools = [calculator, formulate_answer]
    app = get_graph(llm, tools)

    # messages = [
    #     (
    #         "system",
    #         "You are an intelligent agent that can use tools to answer user questions.",
    #     ),
    #     (
    #         "human",
    #         "What is 15 plus 30?",
    #     ),
    # ]

    messages = [
        SystemMessage(
            content="You are an intelligent agent that can use tools to answer user questions."
        ),
        HumanMessage(content="What is 15 plus 30?"),
    ]

    state = State(
        messages=messages,
        remaining_steps=5,
    )

    result = app.invoke(state)
    print(f"Final result: {result}")
    for msg in result["messages"]:
        msg.pretty_print()
