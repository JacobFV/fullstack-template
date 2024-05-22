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


# Verifier
class UserThatRequestsVerificationBase(UserBase):
    pass


class UserThatRequestsVerificationCreate(UserCreate):
    stripe_user_access_token: str | None = None


class UserThatRequestsVerificationUpdate(UserUpdate):
    pass


class UserThatRequestsVerificationUpdateMe(UserUpdateMe):
    stripe_user_access_token: str | None = None


class UserThatRequestsVerification(User):
    verification_requests: list[Verification] = Relationship(
        back_populates="verification_requested_by"
    )
    stripe_user_access_token: str | None = None


class UserThatRequestsVerificationPublic(UserPublic):
    pass


class UserThatRequestsVerificationPublicMe(UserPublicMe):
    verification_requests: list[Verification]
