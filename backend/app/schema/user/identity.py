from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from enum import Enum
from functools import cached_property
from typing import ClassVar, Optional

from pydantic.config import ConfigDict
from sqlalchemy import Column, String, func
from sqlalchemy.ext.hybrid import hybrid_column
from sqlmodel import Field, Relationship, Session, SQLModel, delete, select
from typing_extensions import Unpack

from app.core.redis import get_redis_connection
from app.schema.crud_base import (
    ModelBase,
    ModelCreate,
    ModelInDB,
    ModelRead,
    ModelUpdate,
)


class IdentityBase(ModelBase):
    pass


class IdentityCreate(IdentityBase, ModelCreate):
    image: Optional[bytes]


class IdentityUpdate(IdentityBase, ModelUpdate):
    pass


class Identity(IdentityBase, ModelInDB, table=True):
    id: int | None = Field(default=None, primary_key=True, autoincrement=True)
    image: Optional[bytes]


class IdentityRead(IdentityBase, ModelRead):
    id: int
    image: Optional[bytes]
