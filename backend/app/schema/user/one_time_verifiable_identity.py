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
from app.schema.user.verifiable_identity import (
    VerifiableIdentity,
    VerifiableIdentityBase,
    VerifiableIdentityCreate,
    VerifiableIdentityUpdate,
    VerifiableIdentityUpdateMe,
)


class OneTimeVerifiableIdentityBase(VerifiableIdentityBase):
    pass


class OneTimeVerifiableIdentityCreate(
    OneTimeVerifiableIdentityBase, VerifiableIdentityCreate
):
    pass


class OneTimeVerifiableIdentityUpdate(
    OneTimeVerifiableIdentityBase, VerifiableIdentityUpdate
):
    pass


class OneTimeVerifiableIdentityUpdateMe(
    OneTimeVerifiableIdentityBase, VerifiableIdentityUpdateMe
):
    pass


class OneTimeVerifiableIdentity(OneTimeVerifiableIdentityBase, VerifiableIdentity):
    pass


class OneTimeVerifiableIdentityPublic(VerifiableIdentityPublic):
    pass


class OneTimeVerifiableIdentityPublicMe(VerifiableIdentityPublicMe):
    pass
