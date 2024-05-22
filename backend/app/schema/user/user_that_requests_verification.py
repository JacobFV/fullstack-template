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
from app.schema.user.user import (
    User,
    UserBase,
    UserCreate,
    UserPublic,
    UserPublicMe,
    UserUpdate,
    UserUpdateMe,
)
from app.schema.verification.verification import Verification


# Verifier
class UserThatRequestsVerificationBase(UserBase):
    pass


class UserThatRequestsVerificationCreate(UserThatRequestsVerificationBase, UserCreate):
    stripe_user_access_token: str | None = None


class UserThatRequestsVerificationUpdate(UserThatRequestsVerificationBase, UserUpdate):
    pass


class UserThatRequestsVerificationUpdateMe(
    UserThatRequestsVerificationBase, UserUpdateMe
):
    stripe_user_access_token: str | None = None


class UserThatRequestsVerification(UserThatRequestsVerificationBase, User, table=True):
    verification_requests: list[Verification] = Relationship(
        back_populates="verification_requested_by"
    )
    stripe_user_access_token: str | None = None


class UserThatRequestsVerificationPublic(UserThatRequestsVerificationBase, UserPublic):
    pass


class UserThatRequestsVerificationPublicMe(UserPublicMe):
    verification_requests: list[Verification]
