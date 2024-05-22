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
from app.schema.crud_base import (
    ModelBase,
    ModelCreate,
    ModelInDB,
    ModelRead,
    ModelUpdate,
)
from app.schema.has_redis import HasReddisChannel
from app.schema.user.user import User
from app.schema.user.developer import Developer


class VerificationStatus(Enum):
    REQUESTED = "requested"
    IN_PROGRESS = "in_progress"
    VERIFIED = "verified"
    FAILED = "failed"


class VerificationBase(ModelBase):
    pass


# TODO: change on_completion_webhook_url and on_completion_redirect_url to URLStr when sqlmodel supports it
class VerificationRequestBase(VerificationBase, ModelCreate):
    who_to_verify_id: int
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None


class Verification(HasReddisChannel, VerificationBase, ModelInDB, table=True):
    verification_requested_by_id: int
    verification_requested_by: Developer
    who_to_verify_id: int
    who_to_verify: User
    verf_status: VerificationStatus
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None


class VerificationPublic(VerificationBase, ModelRead):
    verification_requested_by_id: int
    verification_requested_by: Developer
    who_to_verify_id: int
    who_to_verify: User
    verf_status: VerificationStatus
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None
