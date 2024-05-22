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
from app.schema.system.api_key import APIKey, APIKeyRead
from app.schema.user.user import (
    User,
    UserBase,
    UserCreate,
    UserRead,
    UserPublicMe,
    UserUpdate,
    UserUpdateMe,
)
from app.schema.verification.verification import Verification
from app.utils.crud import build_crud_endpoints


# Verifier
class DeveloperBase(UserBase):
    pass


class DeveloperCreate(DeveloperBase, UserCreate):
    stripe_user_access_token: str | None = None


class DeveloperRead(DeveloperBase, UserRead):
    verification_requests: list[Verification] = Field(
        schema_extra={"permission": "self"}  # TODO: implement auth in a base class
    )
    api_keys: list[APIKeyRead] = Field(schema_extra={"view_privileges": "self"})


class DeveloperUpdate(DeveloperBase, UserUpdate):
    stripe_user_access_token: str | None = None


class Developer(DeveloperBase, User, table=True):
    verification_requests: list[Verification] = Relationship(
        back_populates="verification_requested_by"
    )
    stripe_user_access_token: str | None = None
    api_keys: list[APIKey]


crud_router = build_crud_endpoints(
    t_model_base=DeveloperBase,
    t_model_create=DeveloperCreate,
    t_model_read=DeveloperRead,
    t_model_update=DeveloperUpdate,
    t_model_in_db=Developer,
)
