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
from app.schema.base import ModelBase
from app.schema.user.identity import (
    Identity,
    IdentityBase,
    IdentityCreate,
    IdentityRead,
    IdentityUpdate,
)
from app.utils.crud import build_crud_endpoints


# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(IdentityBase):
    email: str = Field(unique=True, index=True)
    is_active: bool = Field(True)
    is_superuser: bool = Field(False)
    full_name: str | None = Field(None)


# Properties to receive via API on creation
class UserCreate(IdentityCreate, UserBase):
    password: str = Field()


# TODO replace email str with EmailStr when sqlmodel supports it
class UserRegister(ModelBase):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(IdentityUpdate, UserBase):
    email: str | None = Field(None)  # type: ignore
    password: str | None = Field(None)
    full_name: str | None = Field(None)


# Properties to return via API, id is always required
class UserRead(IdentityRead, UserBase):
    email: str = Field(unique=True, index=True)
    is_active: bool = Field(True)
    is_superuser: bool = Field(False)
    full_name: str | None = Field(None)


# Database model, database table inferred from class name
class User(Identity, UserBase):
    hashed_password: str = Field()


# other API models
class UpdatePassword(ModelBase):
    current_password: str
    new_password: str


crud_router = build_crud_endpoints(
    t_model_base=UserBase,
    t_model_create=UserCreate,
    t_model_read=UserRead,
    t_model_update=UserUpdate,
    t_model_in_db=User,
)
