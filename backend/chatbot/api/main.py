import logging
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chatbot.api.routes import router
from chatbot.api.routes_auth import router_login

app = FastAPI(title="Example API", version="0.1.0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Autoriser le frontend (dev)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://frontend:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
app.include_router(router_login)


@app.get("/health", response_model=Dict[str, str], tags=["Root"])
def read_root():
    return {"status": "ok"}
