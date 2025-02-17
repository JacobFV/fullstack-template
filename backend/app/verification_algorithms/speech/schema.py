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
from app.verification_algorithms.base.schema import (
    Verification,
    VerificationBase,
    VerificationRead,
    VerificationCreate,
    VerificationUpdate,
)
from app.utils.crud import build_crud_endpoints


class HumanSpeechVerificationBase(VerificationBase):
    model_name: str = "human_speech_verification-001"


class HumanSpeechVerificationRequest(HumanSpeechVerificationBase, VerificationCreate):
    pass


class HumanSpeechVerificationRead(HumanSpeechVerificationBase, VerificationRead):
    model_name = Field(
        "human_speech_verification-001",
        schema_extra={"view_privileges": ModelRead.Privileges.owner},
    )


class HumanSpeechVerificationUpdate(HumanSpeechVerificationBase, VerificationUpdate):
    pass


class HumanSpeechVerification(HumanSpeechVerificationBase, Verification):
    pass


crud_router = build_crud_endpoints(
    t_model_base=HumanSpeechVerificationBase,
    t_model_create=HumanSpeechVerificationRequest,
    t_model_read=HumanSpeechVerificationRead,
    t_model_update=HumanSpeechVerificationUpdate,
    t_model_in_db=HumanSpeechVerification,
)
