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
from app.schema.crud_base import CRUDBase, CRUDCreate, CRUDInDB, CRUDRead, CRUDUpdate


class IdentityBase(CRUDBase):
    pass


class IdentityCreate(IdentityBase, CRUDCreate):
    image: Optional[bytes]


class IdentityUpdate(IdentityBase, CRUDUpdate):
    pass


class Identity(IdentityBase, CRUDInDB, table=True):
    id: int | None = Field(default=None, primary_key=True, autoincrement=True)
    image: Optional[bytes]


class IdentityRead(IdentityBase, CRUDRead):
    id: int
    image: Optional[bytes]
