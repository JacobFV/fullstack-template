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

class VerificationStatus(Enum):
    REQUESTED = "requested"
    IN_PROGRESS = "in_progress"
    VERIFIED = "verified"
    FAILED = "failed"


class VerificationBase(ModelBase):
    pass


class VerificationRequestBase(VerificationBase, ModelCreate):
    who_to_verify_id: int
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None


class VerificationRead(VerificationBase, ModelRead):
    verification_requested_by_id: int
    verification_requested_by: DeveloperRead
    who_to_verify_id: int
    who_to_verify: User
    verf_status: VerificationStatus
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None


class VerificationUpdate(VerificationBase, ModelUpdate):
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None

class Verification(HasReddisChannel, VerificationBase, ModelInDB):
    verification_requested_by_id: int
    verification_requested_by: Developer
    who_to_verify_id: int
    who_to_verify: User
    verf_status: VerificationStatus
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None

    class Config:
        table = True

    @property
    def verification_requested_by(self):
        from app.schema.user import Developer
        return Developer

    @property
    def who_to_verify(self):
        from app.schema.user import User
        return User

def build_crud_endpoints(t_model_base: type[SQLModel], t_model_create: type[SQLModel],
                        t_model_read: type[SQLModel], t_model_in_db: type[SQLModel]) -> None:
    # Implementation of build_crud_endpoints function
    pass

crud_router = build_crud_endpoints(
    t_model_base=VerificationBase,
    t_model_create=VerificationRequestBase,
    t_model_read=VerificationRead,
    t_model_in_db=Verification,
)