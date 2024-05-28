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
from app.schema.user.developer import Developer, DeveloperRead, User

from app.core.redis import get_redis_connection
from app.schema.base import (
    ModelBase,
    ModelCreate,
    ModelInDB,
    ModelRead,
    ModelUpdate,
)
from app.schema.has_redis import HasReddisChannel
from app.schema.user.developer import DeveloperRead, Developer
from app.schema.user.identity import IdentityRead, Identity
from app.utils.context import Context


class VerificationStatus(Enum):
    REQUESTED = "requested"
    IN_PROGRESS = "in_progress"
    VERIFIED = "verified"
    FAILED = "failed"


class VerificationBase(ModelBase):
    pass


class VerificationRequestBase(VerificationBase, ModelCreate):
    requester_id: int
    target_id: int
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None


def requester_or_target_can_read_fn(
    read_model: "VerificationRead", context: Context
) -> bool:
    return (
        context.user.id == read_model.requester_id
        or context.user.id == read_model.target_id
    )


class VerificationRead(VerificationBase, ModelRead):
    requester_id: int = Field(
        schema_extras={"can_read": requester_or_target_can_read_fn}
    )
    # yes, use nested models here
    requester: DeveloperRead = Field(
        schema_extras={"can_read": requester_or_target_can_read_fn}
    )
    target_id: int = Field(schema_extras={"can_read": requester_or_target_can_read_fn})
    # yes, use nested models here
    target: IdentityRead = Field(
        schema_extras={"can_read": requester_or_target_can_read_fn}
    )
    verf_status: VerificationStatus = Field(
        schema_extras={"can_read": requester_or_target_can_read_fn}
    )
    on_completion_webhook_url: str = Field(
        schema_extras={"can_read": requester_or_target_can_read_fn}
    )
    on_completion_redirect_url: str | None = Field(
        None, schema_extras={"can_read": requester_or_target_can_read_fn}
    )


def requester_or_target_can_update_fn(
    update_model: "VerificationUpdate",
    db_model: "Verification",
    context: Context,
) -> bool:
    return (
        context.user.id == db_model.requester_id
        or context.user.id == db_model.target_id
    )


class VerificationUpdate(VerificationBase, ModelUpdate):
    on_completion_webhook_url: str = Field()
    on_completion_redirect_url: str | None = Field(None)


class Verification(HasReddisChannel, VerificationBase, ModelInDB, table=True):
    requester_id: int = Field(foreign_key=Developer.id)
    requester: Developer = Relationship(back_populates="verifications_requested")
    target_id: int = Field(foreign_key=Identity.id)
    target: Identity = Relationship(back_populates="verifications_targeted")
    verf_status: VerificationStatus = Field()
    on_completion_webhook_url: str = Field()
    on_completion_redirect_url: Optional[str] = Field()


crud_router = build_crud_endpoints(
    t_model_base=VerificationBase,
    t_model_create=VerificationRequestBase,
    t_model_read=VerificationRead,
    t_model_update=VerificationUpdate,
    t_model_in_db=Verification,
)
