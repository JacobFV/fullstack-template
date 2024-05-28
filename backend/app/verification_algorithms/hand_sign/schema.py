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
from app.verification_algorithms.base.verification import (
    Verification,
    VerificationBase,
    VerificationRead,
    VerificationCreate,
    VerificationUpdate,
)
from app.utils.crud import build_crud_endpoints
from app.schema.base import ModelRead


class HandSignVerificationBase(VerificationBase):
    model_name: str = "hand_sign_verification-001"


class HandSignVerificationRequest(HandSignVerificationBase, VerificationCreate):
    pass


class HandSignVerificationRead(HandSignVerificationBase, VerificationRead):
    model_name = Field(
        "hand_sign_verification-001",
        schema_extra={"view_privileges": ModelRead.Privileges.owner},
    )
    hand_symbols: list[str]


class HandSignVerificationUpdate(HandSignVerificationBase, VerificationUpdate):
    pass


class HandSignVerification(HandSignVerificationBase, Verification):
    hand_symbols: list[str]


crud_router = build_crud_endpoints(
    t_model_base=HandSignVerificationBase,
    t_model_create=HandSignVerificationRequest,
    t_model_read=HandSignVerificationRead,
    t_model_in_db=HandSignVerification,
)
