from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging

from chatbot.api.routes import router

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

# class Item(BaseModel):
#     id: int
#     name: str
#     description: str | None = None


# # Petite "base" en mémoire
# DB: list[Item] = []


# @app.get("/")
# def read_root():
#     return {"message": "Hello from FastAPI"}


# @app.post("/items", response_model=Item)
# def create_item(item: Item):
#     DB.append(item)
#     logger.info(f"Item added: {item}")
#     return item


# @app.get("/items")
# def list_items():
#     return DB
