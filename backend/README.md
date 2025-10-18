# chatbot

Simple chatbot with FastAPI. This project aims to develop my skills with FastAPI, multi-agent architecture, and high interaction with the user.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)

---

## Overview

This project is a simple chatbot backend built with FastAPI. It supports agent-based conversations, SQLite-based checkpointing, and is designed for extensibility.

## Features

- FastAPI backend for chatbot interactions
- Mock agent for development/testing
- SQLite-based checkpointing for conversation persistence
- Extensible agent architecture
- API routes for chatting and retrieving conversation threads

## Architecture

- Python 3.11+ (see `pyproject.toml`)
- FastAPI for API layer
- SQLite for persistence
- Modular codebase (`chatbot/agent`, `chatbot/api`, `chatbot/messages`, `chatbot/services`)
- Docker support for deployment

## Installation

### Prerequisites

- Python 3.11+ (recommended: use `uv` for environment management)
- Docker (optional, for containerized deployment)

### Steps

1. `uv venv --python 3.11`
2. `source .venv/bin/activate`
3. `uv pip install -r requirements.lock`

## Usage

### Running the API server

```bash
uvicorn chatbot.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

Build and run the Docker container:
```bash
docker build -t chatbot .
docker run -p 8000:8000 chatbot
```

## Concepts
### Conversation Threads


A **thread** represents a conversation between the user and the system, identified by a unique `thread_id` and containing a list of messages (`conversation`).

#### Thread Model

```python
class Thread(BaseModel):
        thread_id: str  # Unique identifier for the thread
        conversation: List[MessageOut]  # List of messages in the conversation
```

#### MessageOut Model

```python
class MessageOut(BaseModel):
        id: str  # Unique identifier for the message
        author: Author  # One of: user, agent, tool, system
        content: str  # Content of the message
        timestamp: date  # When the message was created
```

#### Example Thread Object

```json
{
    "thread_id": "abc123",
    "conversation": [
        {
            "id": "msg1",
            "author": "user",
            "content": "Hello!",
            "timestamp": "2025-10-18"
        },
        {
            "id": "msg2",
            "author": "agent",
            "content": "Hi, how can I help you today?",
            "timestamp": "2025-10-18"
        }
    ]
}
```

**Fields:**
- `thread_id`: Unique string identifying the conversation thread.
- `conversation`: List of messages, each with:
    - `id`: Unique message ID
    - `author`: One of `user`, `agent`, `tool`, `system`
    - `content`: Message text
    - `timestamp`: ISO date string

## API Reference

TODO: Fill in details about the API endpoints, request/response formats, and example payloads.

- `/agent/chat/{thread_id}`: Chat with an agent (optionally specify agent id)
- `/thread/{thread_id}`: Retrieve the entire conversation thread

## Configuration

TODO: Fill in details about environment variables, config files, or settings required for deployment or development.

## Development
### TODO
See the full development to-do list in [TODO.md](./TODO.md)

## Testing

Run backend tests:
```bash
pytest
```
TODO: Add more details about test coverage, test files, and how to run frontend tests if applicable.

## Deployment

- Dockerfile provided for containerized deployment
- Exposes port 8000
- CMD: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
TODO: Fill in details about deployment to cloud providers, CI/CD, or other environments.

<!-- ## Contributing

TODO: Add guidelines for contributing, code style, pull requests, etc. -->

<!-- ## License

TODO: Specify the license for your project (MIT, Apache, etc.) -->

<!-- ## Acknowledgements

TODO: Credit any libraries, tutorials, or contributors. -->
