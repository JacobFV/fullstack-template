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
from app.schema.crud_base import ModelBase
from app.schema.user.identity import (
    Identity,
    IdentityBase,
    IdentityCreate,
    IdentityRead,
    VerifiableIdentityPublicMe,
    IdentityUpdate,
    VerifiableIdentityUpdateMe,
)


# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(IdentityBase):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class UserCreate(IdentityCreate, UserBase):
    password: str


# TODO replace email str with EmailStr when sqlmodel supports it
class UserRegister(ModelBase):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(IdentityUpdate, UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None
    full_name: str | None = None


class UpdatePassword(ModelBase):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(Identity, UserBase):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


# Properties to return via API, id is always required
class UserRead(IdentityRead, UserBase):
    id: int
