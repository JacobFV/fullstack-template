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
from app.schema.user.ownership import owner_can_read

from app.schema.user.user import (
    User,
    UserBase,
    UserCreate,
    UserRead,
    UserPublicMe,
    UserUpdate,
    UserUpdateMe,
)
from app.utils.context import Context
from app.verification_algorithms.base.schema import Verification
from app.utils.crud import build_crud_endpoints
from app.schema.system.api_key import APIKey, APIKeyRead


class DeveloperBase(UserBase):
    pass


class DeveloperCreate(DeveloperBase, UserCreate):
    pass


class DeveloperRead(DeveloperBase, UserRead):
    verification_requests: list[Verification] = Field(
        schema_extra={UserRead.PRIVILEGES_FIELD_KEY: owner_can_read}
    )
    api_keys: list[APIKeyRead] = Field(
        schema_extra={"view_privileges": "self"}
    )  # yes, nested models here


class DeveloperUpdate(DeveloperBase, UserUpdate):
    pass


class Developer(DeveloperBase, User, table=True):
    verification_requests: list[Verification] = Relationship(
        back_populates="verification_requested_by"
    )
    stripe_user_access_token: str | None = Field(None, exclude=True)
    api_keys: list[APIKey] = Relationship(back_populates="owner")

    @classmethod
    def from_create(
        cls,
        model_create: DeveloperCreate,
        context: "Context",
        extra_keys: Optional[dict] = None,
        commit=True,
        refresh=True,
    ) -> Developer:
        developer_in_db = super().from_create(
            model_create=model_create,
            context=context,
            extra_keys=extra_keys,
            commit=commit,
            refresh=refresh,
        )
        return developer_in_db

    def update_from(
        self,
        model_update: UserUpdate,
        context: Context,
        extra_keys: dict | None = None,
        commit=True,
        refresh=False,
    ) -> None:
        return super().update_from(
            model_update=model_update,
            context=context,
            extra_keys=extra_keys,
            commit=commit,
            refresh=refresh,
        )

    def to_read(self, context: Context, refresh=False) -> DeveloperRead:
        return super().to_read(context, refresh=refresh)
