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
from app.schema.user.identity import (
    IdentityBase,
    IdentityCreate,
    IdentityRead,
    IdentityUpdate,
    Identity,
)
from app.utils.crud import build_crud_endpoints


class GhostIdentityBase(IdentityBase):
    pass


class GhostIdentityCreate(GhostIdentityBase, IdentityCreate):
    pass


class GhostIdentityRead(IdentityRead):
    pass


class GhostIdentityUpdate(GhostIdentityBase, IdentityUpdate):
    pass


class GhostIdentity(GhostIdentityBase, Identity):
    pass


crud_router = build_crud_endpoints(
    t_model_base=GhostIdentityBase,
    t_model_create=GhostIdentityCreate,
    t_model_read=GhostIdentityRead,
    t_model_update=GhostIdentityUpdate,
    t_model_in_db=GhostIdentity,
)
