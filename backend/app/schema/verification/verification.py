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


class VerificationRead(VerificationBase, ModelRead):
    requester_id: int
    requester: DeveloperRead
    target_id: int
    target: IdentityRead
    verf_status: VerificationStatus
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None


class VerificationUpdate(VerificationBase, ModelUpdate):
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None


class Verification(HasReddisChannel, VerificationBase, ModelInDB, table=True):
    requester_id: int
    requester: Developer
    target_id: int
    target: Identity
    verf_status: VerificationStatus
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None


crud_router = build_crud_endpoints(
    t_model_base=VerificationBase,
    t_model_create=VerificationRequestBase,
    t_model_read=VerificationRead,
    t_model_update=VerificationUpdate,
    t_model_in_db=Verification,
)
