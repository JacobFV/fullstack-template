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
from app.schema.base import (
    CreatePrivileges,
    ModelBase,
    ModelCreate,
    ModelInDB,
    ModelRead,
    ModelUpdate,
    ReadPrivileges,
    UpdatePrivileges,
    nobody_can_update,
)
from app.schema.has_redis import HasReddisChannel
from app.schema.id import ID
from app.schema.user.developer import DeveloperRead, Developer
from app.schema.user.identity import IdentityRead, Identity
from app.utils.context import Context
from app.schema.user.ownership import (
    HasOwner,
    HasOwnerBase,
    HasOwnerCreate,
    HasOwnerRead,
    HasOwnerUpdate,
    owner_can_create,
    owner_can_delete,
    owner_can_read,
    owner_can_update,
)


class VerificationStatus(Enum):
    REQUESTED = "requested"
    IN_PROGRESS = "in_progress"
    VERIFIED = "verified"
    FAILED = "failed"


def owner_or_target_can_read_fn(
    read_model: "VerificationRead", context: Context
) -> bool:
    return (
        context.user.id == read_model.owner_id
        or context.user.id == read_model.target_id
    )


def owner_or_target_can_update_fn(
    update_model: "VerificationUpdate",
    db_model: "Verification",
    context: Context,
) -> bool:
    return context.user.id == db_model.owner_id or context.user.id == db_model.target_id


class VerificationBase(HasOwnerBase, ModelBase):
    owner_id: Identity.ID = Field(
        schema_extra={
            ModelRead.PRIVILEGES_KEY: owner_or_target_can_read_fn,
            ModelUpdate.PRIVILEGES_KEY: nobody_can_update,
        }
    )


class VerificationCreate(VerificationBase, HasOwnerCreate, ModelCreate):
    target_id: Identity.ID
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None

    OBJECT_CREATE_PRIVILEGES: ClassVar[CreatePrivileges] = owner_can_create


class VerificationRead(VerificationBase, HasOwnerRead, ModelRead):
    # yes, use nested models here
    target_id: Identity.ID = Field(schema_extras={"can_read": owner_or_target_can_read_fn})
    # yes, use nested models here
    target: IdentityRead = Field(
        schema_extras={
            ModelRead: owner_or_target_can_read_fn,
        }
    )
    verf_status: VerificationStatus = Field(
        schema_extras={
            ModelRead: owner_or_target_can_read_fn,
        }
    )
    on_completion_webhook_url: str = Field(
        schema_extras={
            ModelRead: owner_or_target_can_read_fn,
        }
    )
    on_completion_redirect_url: str | None = Field(
        None,
        schema_extras={
            ModelRead: owner_or_target_can_read_fn,
        },
    )

    DEFAULT_FIELD_PRIVILEGES: ClassVar[ReadPrivileges] = owner_can_read
    OBJECT_READ_PRIVILEGES: ClassVar[ReadPrivileges] = owner_can_read


class VerificationUpdate(VerificationBase, HasOwnerUpdate, ModelUpdate):
    on_completion_webhook_url: str = Field(
        schema_extra={
            ModelUpdate.PRIVILEGES_KEY: owner_can_update,
        }
    )
    on_completion_redirect_url: str | None = Field(
        None,
        schema_extra={
            ModelUpdate.PRIVILEGES_KEY: owner_can_update,
        },
    )

    DEFAULT_FIELD_PRIVILEGES: ClassVar[UpdatePrivileges] = owner_can_update
    OBJECT_UPDATE_PRIVILEGES: ClassVar[UpdatePrivileges] = owner_can_update


class Verification(HasReddisChannel, VerificationBase, HasOwner, ModelInDB, table=True):
    requester_id: Developer.ID = Field(foreign_key=Developer.id)
    requester: Developer = Relationship(back_populates="verifications_requested")
    target_id: Identity.ID = Field(foreign_key=Identity.id)
    target: Identity = Relationship(back_populates="verifications_targeted")
    verf_status: VerificationStatus = Field(default=VerificationStatus.REQUESTED)
    on_completion_webhook_url: str = Field()
    on_completion_redirect_url: Optional[str] = Field()

    OBJECT_DELETE_PRIVILEGES: ClassVar[UpdatePrivileges] = owner_can_delete

    @classmethod
    def from_create(
        cls,
        model_create: HasOwnerCreate,
        context: Context,
        extra_keys: dict | None = None,
        commit=True,
        refresh=True,
    ) -> HasOwner:
        return super().from_create(model_create, context, extra_keys, commit, refresh)

    def update_from(
        self,
        model_update: ModelUpdate,
        context: Context,
        extra_keys: dict | None = None,
        commit=True,
        refresh=False,
    ) -> None:
        return super().update_from(model_update, context, extra_keys, commit, refresh)

    def to_read(self, context: Context, refresh=False) -> VerificationRead:
        return super().to_read(context, refresh=refresh)


crud_router = build_crud_endpoints(
    t_model_base=VerificationBase,
    t_model_create=VerificationCreate,
    t_model_read=VerificationRead,
    t_model_update=VerificationUpdate,
    t_model_in_db=Verification,
)
