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
from app.schema.base import ModelInDB


class HasReddisChannel(ModelInDB, table=False):

    @property
    def redis_channel_name(self) -> str:
        return f"redis_{func.lower(self.__class__.__name__)}_{self.id}"

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
