from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, Request
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.pregel import Pregel

from chatbot.agent.main import get_agents_dict
from chatbot.config import config

HERE = Path(__file__).parent


@dataclass
class AgentLifespanState:
    """Global state for the lifespan of the application."""

    agent_dict: Dict[str, Pregel]
    checkpointer: AsyncSqliteSaver | SqliteSaver


def get_state(request: Request) -> AgentLifespanState:
    return request.app.state.state


def _patch_async_checkpointer_connection(checkpointer: AsyncSqliteSaver) -> None:
    """Backwards-compat shim for langgraph-checkpoint-sqlite + aiosqlite>=0.22."""
    conn: Any = checkpointer.conn
    if callable(getattr(conn, "is_alive", None)):
        return

    # aiosqlite>=0.22 dropped Thread inheritance; langgraph still expects is_alive.
    setattr(conn, "is_alive", lambda: bool(getattr(conn, "_running", True)))


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    CHECKPOINT_SQLITE = f"{HERE}/../../data/checkpoint_app.db"
    async with AsyncSqliteSaver.from_conn_string(CHECKPOINT_SQLITE) as checkpointer:
        _patch_async_checkpointer_connection(checkpointer)

        agent_dict: Dict[str, Pregel] = await get_agents_dict(
            checkpointer=checkpointer, verbose=config.verbose, mock=config.mock
        )

        app.state.state = AgentLifespanState(
            agent_dict=agent_dict, checkpointer=checkpointer
        )

        yield
