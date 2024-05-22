from __future__ import annotations
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from functools import cached_property
from typing import ClassVar, Optional
from typing_extensions import Unpack
from app.core.redis import get_redis_connection
from pydantic.config import ConfigDict
from sqlalchemy import func
from sqlalchemy import Column, String

from sqlmodel import Field, Relationship, Session, SQLModel, select, delete


class VerificationStatus(Enum):
    REQUESTED = "requested"
    IN_PROGRESS = "in_progress"
    VERIFIED = "verified"
    FAILED = "failed"


class VerificationBase(CRUDBase):
    pass


# TODO: change on_completion_webhook_url and on_completion_redirect_url to URLStr when sqlmodel supports it
class VerificationRequestBase(VerificationBase, CRUDCreate):
    who_to_verify_id: int
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None


class Verification(HasReddisChannel, VerificationBase, CRUDInDB):
    verification_requested_by_id: int
    verification_requested_by: UserThatRequestsVerification
    who_to_verify_id: int
    who_to_verify: User
    verf_status: VerificationStatus
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None


class VerificationPublic(VerificationBase, CRUDRead):
    verification_requested_by_id: int
    verification_requested_by: UserThatRequestsVerification
    who_to_verify_id: int
    who_to_verify: User
    verf_status: VerificationStatus
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None
