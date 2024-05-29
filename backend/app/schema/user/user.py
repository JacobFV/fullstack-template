from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from enum import Enum
from functools import cached_property
from typing import ClassVar, Optional
from backend.app.core.security import verify_password

from pydantic.config import ConfigDict
from sqlalchemy import Column, String, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlmodel import Field, Relationship, Session, SQLModel, delete, select
from typing_extensions import Unpack

from app.core.redis import get_redis_connection
from app.schema.base import ModelBase, ModelCreate, ModelRead, ModelUpdate, ModelInDB
from app.schema.user.identity import (
    Identity,
    IdentityBase,
    IdentityCreate,
    IdentityRead,
    IdentityUpdate,
)
from app.schema.user.ownership import owner_can_read, owner_can_update
from app.utils.context import Context
from app.utils.crud import build_crud_endpoints


# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(IdentityBase):
    email: str = Field(unique=True, index=True)
    is_active: bool = Field(True)
    is_superuser: bool = Field(False)
    full_name: str | None = Field(None)


# Properties to receive via API on creation
# TODO replace email str with EmailStr when sqlmodel supports it
class UserCreate(IdentityCreate, UserBase):
    email: str
    password: str
    full_name: str | None = None


# Properties to return via API, id is always required
class UserRead(IdentityRead, UserBase):
    email: str = Field(
        unique=True,
        index=True,
        schema_extra={
            # TODO: make fields for is_email_public,
            # and update the field privilege interface
            # to support accepting the *InDB arg to
            # check other fields not in the read model
            ModelRead.PRIVILEGES_KEY: owner_can_read
        },
    )
    is_active: bool = Field(True)
    is_superuser: bool = Field(False)
    full_name: str | None = Field(
        None,
        schema_extra={
            # TODO: make fields for is_email_public,
            # and update the field privilege interface
            # to support accepting the *InDB arg to
            # check other fields not in the read model
            ModelRead.PRIVILEGES_KEY: owner_can_read
        },
    )


# Properties to receive via API on update, all are optional
class UserUpdate(IdentityUpdate, UserBase):
    # TODO replace email str with EmailStr when sqlmodel supports it
    email: str | None = Field(None)  # type: ignore
    new_password: str | None = Field(
        None, schema_extra={ModelUpdate.PRIVILEGES_KEY: owner_can_update}
    )
    full_name: str | None = Field(None)

    DEFAULT_FIELD_PRIVILEGES = owner_can_update
    OBJECT_UPDATE_PRIVILEGES = owner_can_update


# Database model, database table inferred from class name
class User(Identity, UserBase):
    hashed_password: str = Field()

    @classmethod
    def from_create(
        cls,
        model_create: UserCreate,
        context: "Context",
        extra_keys: Optional[dict] = None,
        commit=True,
        refresh=True,
    ) -> User:
        hashed_password = hash_password(model_create.password)
        user_in_db = super().from_create(
            model_create=model_create,
            context=context,
            extra_keys={"hashed_password": hashed_password, **(extra_keys or {})},
            commit=commit,
            refresh=refresh,
        )
        return user_in_db

    def update_from(
        self,
        model_update: UserUpdate,
        context: "Context",
        extra_keys: Optional[dict] = None,
        commit=True,
        refresh=False,
    ) -> None:
        extra_keys = extra_keys or {}

        if model_update.new_password:
            hashed_password = hash_password(model_update.new_password)
            extra_keys["hashed_password"] = hashed_password
            model_update.new_password = None

        super().update_from(
            model_update=model_update,
            context=context,
            extra_keys=extra_keys,
            commit=commit,
            refresh=refresh,
        )

    def to_read(self, context: Context, refresh=False) -> UserRead:
        return super().to_read(context, refresh=refresh)

    @classmethod
    def find_by_email(cls, *, session: Session, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        session_user = session.exec(statement).first()
        return session_user

    def authenticate(self, password: str) -> bool:
        return verify_password(password, self.hashed_password)


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
