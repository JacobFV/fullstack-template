from __future__ import annotations
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from functools import cached_property
from typing import ClassVar, Optional
from typing_extensions import Unpack
from app.core.redis import get_redis_connection
from pydantic.config import ConfigDict
from sqlalchemy import func
from sqlalchemy import Column, String

from sqlmodel import Field, Relationship, Session, SQLModel, select, delete


# Shared properties
class ItemBase(CRUDBase):
    title: str
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase, CRUDCreate):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase, CRUDUpdate):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, CRUDInDB):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase, CRUDRead):
    id: int
    owner_id: int


class ItemsPublic(CRUDBase):
    data: list[ItemPublic]
    count: int
