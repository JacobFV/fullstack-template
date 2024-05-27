from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from enum import Enum
from functools import cached_property
from typing import ClassVar, Optional

from pydantic.config import ConfigDict
from sqlalchemy import Column, String, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlmodel import Field, Relationship, Session, SQLModel, delete, select
from typing_extensions import Unpack

from app.core.redis import get_redis_connection
from app.schema.base import ModelInDB

class HasReddisChannel(ModelInDB):
    _redis_channel_name: str = Column(String, name="redis_channel_name")

    @hybrid_property
    def redis_channel_name(self) -> str:
        return self._redis_channel_name

    @redis_channel_name.setter
    def redis_channel_name(self, value: str):
        self._redis_channel_name = value

    @redis_channel_name.expression
    def redis_channel_name(cls) -> str: 
        from sqlalchemy import func
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
