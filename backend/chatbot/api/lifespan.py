from contextlib import asynccontextmanager
from dataclasses import dataclass
from fastapi import Request, FastAPI
from pathlib import Path

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.pregel import Pregel
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.checkpoint.sqlite import SqliteSaver


from chatbot.agent.main import get_agent

HERE = Path(__file__).parent


@dataclass
class AgentLifespanState:
    """Global state for the lifespan of the application."""

    agent: Pregel
    checkpointer: AsyncSqliteSaver | SqliteSaver


def get_state(request: Request) -> AgentLifespanState:
    return request.app.state.state


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

    CHECKPOINT_SQLITE = f"{HERE}/../../data/checkpoint_app.db"
    async with AsyncSqliteSaver.from_conn_string(CHECKPOINT_SQLITE) as checkpointer:
        await checkpointer.setup()
        agent = get_agent(checkpointer=checkpointer, verbose=False, mock=True)
        app.state.state = AgentLifespanState(agent=agent, checkpointer=checkpointer)

        yield
