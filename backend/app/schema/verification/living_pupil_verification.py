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
from app.schema.base import ModelBase, ModelRead
from app.schema.verification.verification import (
    Verification,
    VerificationBase,
    VerificationRead,
    VerificationRequestBase,
    VerificationUpdate,
)
from app.utils.crud import build_crud_endpoints


class LivingPupilVerificationBase(VerificationBase):
    model_name: str = "living_pupil_verification-001"


class LivingPupilVerificationRequest(
    LivingPupilVerificationBase, VerificationRequestBase
):
    pass


class LivingPupilVerificationRead(LivingPupilVerificationBase, VerificationRead):
    model_name = Field(
        "living_pupil_verification-001",
        schema_extra={"view_privileges": ModelRead.ViewPrivileges.owner},
    )


class LivingPupilVerificationUpdate(LivingPupilVerificationBase, VerificationUpdate):
    pass


class LivingPupilVerification(LivingPupilVerificationBase, Verification):
    pass


crud_router = build_crud_endpoints(
    t_model_base=LivingPupilVerificationBase,
    t_model_create=LivingPupilVerificationRequest,
    t_model_read=LivingPupilVerificationRead,
    t_model_update=LivingPupilVerificationUpdate,
    t_model_in_db=LivingPupilVerification,
)
