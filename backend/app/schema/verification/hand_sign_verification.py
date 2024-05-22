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
from app.schema.verification.verification import (
    Verification,
    VerificationBase,
    VerificationPublic,
)


class HandSignVerificationBase(VerificationBase):
    model_name: str = "hand_sign_verification-001"


class HandSignVerification(HandSignVerificationBase, Verification):
    hand_letters: list[str]


class HandSignVerificationRead(HandSignVerificationBase, VerificationPublic):
    pass
