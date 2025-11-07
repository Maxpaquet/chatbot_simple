# chatbot_simple

## Overview

This project is a simple chatbot application with a LangGraph + FastAPI backend and a Next.js frontend. It demonstrates API communication, Docker-based development, and a mock agent for testing with LangGraph.

## Project Structure

- `backend/` — FastAPI backend (Python)
	- `app/main.py` — Main FastAPI app with in-memory DB and CORS
	- `chatbot/agent/` — Mock agent and LangGraph graph code
	- `Dockerfile` — Backend Docker build
- `frontend/` — Next.js frontend (JavaScript/React)
	- `pages/index.js` — Main UI, interacts with backend via API proxy
	- `pages/api/items.js` — Next.js API route proxying requests to backend
	- `Dockerfile` — Frontend Docker build
- `docker-compose.yml` — Orchestrates frontend and backend containers

## Development

### Prerequisites
- Docker and Docker Compose
- Node.js (for local frontend dev)
- Python 3.10+ (for local backend dev)

### Running with Docker Compose

1. Build and start all services:
	 ```sh
	 docker compose up --build
	 ```
2. Frontend: http://localhost:3000
3. Backend: http://localhost:8000
4. API docs: http://localhost:8000/docs

### Local Development

#### Backend
```sh
cd backend
pip install -r requirements.lock
uvicorn app.main:app --reload
```

#### Frontend
```sh
cd frontend
npm install
npm run dev
```
Set `NEXT_PUBLIC_API_URL` to your backend URL if needed.

## Features

- Add and list items via a simple UI
- FastAPI backend with in-memory storage
- CORS enabled for local dev and Docker
- Next.js frontend with notification on add
- API proxy route for seamless Docker/browser integration
- Mock agent and graph for testing with LangGraph

## Testing the Backend

- Use Swagger UI at `/docs` for interactive API testing
- Or use curl:
	```sh
	curl -X POST http://localhost:8000/items -H "Content-Type: application/json" -d '{"id":1,"name":"Test","description":"desc"}'
	curl http://localhost:8000/items
	```

## Notes

- For client-side fetches, the frontend uses `/api/items` which proxies to the backend, avoiding CORS and network issues in Docker.
- The backend and frontend communicate via Docker network when using Docker Compose.
- The mock agent in `backend/chatbot/agent/` is for testing and development with LangGraph.