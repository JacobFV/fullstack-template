from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from enum import Enum
from functools import cached_property
from typing import ClassVar, Optional

from pydantic.config import ConfigDict
from sqlalchemy import Column, String, func
from sqlmodel import Field, Relationship, Session, SQLModel, delete, select
from typing_extensions import Unpack

from app.core.redis import get_redis_connection
from app.schema.crud_base import CRUDBase


# JSON payload containing access token
class Token(CRUDBase):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(CRUDBase):
    sub: int | None = None


class NewPassword(CRUDBase):
    token: str
    new_password: str
