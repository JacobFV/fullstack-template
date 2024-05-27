from __future__ import annotations
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from functools import cached_property
from typing import Optional
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy import Column, String, func, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlmodel import SQLModel, Field, Relationship
from typing_extensions import Unpack
import asyncio
from app.core.redis import get_redis_connection

Base: DeclarativeMeta = declarative_base()

class ModelInDB(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

class HasReddisChannel(ModelInDB):
    _redis_channel_name = Column(String, name="redis_channel_name")

    @property
    def redis_channel_name(self) -> str:
        return self._redis_channel_name

    @redis_channel_name.setter
    def redis_channel_name(self, value: str):
        self._redis_channel_name = value

    @classmethod
    def redis_channel_name(cls) -> str:
        return func.concat("redis_", func.lower(cls.__name__), "_", cls.id)
    
    async def publish_message(self, message: str):
        connection = await get_redis_connection()
        await connection.publish(self.redis_channel_name, message)

    @cached_property
    async def redis_channel_listener(self):
        connection = await get_redis_connection()
        pubsub = connection.pubsub()
        await pubsub.subscribe(self.redis_channel_name)
        return pubsub

    async def listen_for_messages(self, message_handler):
        async for message in self.redis_channel_listener.listen():
            if message["type"] == "message":
                await message_handler(message["data"])

# Setup SQLAlchemy engine and session
engine = create_engine("sqlite:///example.db")  # Use your actual DB URL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)
