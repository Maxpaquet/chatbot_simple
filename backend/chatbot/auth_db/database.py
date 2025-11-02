from typing import Dict

from sqlalchemy import Column, Engine, ForeignKey, Integer, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from chatbot.auth_db.utils import DATABASE_URL

# Fake database - replace with real database in production
fake_users_db: Dict = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
        "disabled": False,
    }
}


def get_engine() -> Engine:
    engine: Engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
    return engine


def get_sessionmaker(engine: Engine) -> sessionmaker:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal


Base = declarative_base()


def get_user_roles():
    # Association table for many-to-many relationship between users and roles

    user_roles = Table(
        "user_roles",
        Base.metadata,
        Column("user_id", Integer, ForeignKey("users.id")),
        Column("role_id", Integer, ForeignKey("roles.id")),
    )
    return user_roles
