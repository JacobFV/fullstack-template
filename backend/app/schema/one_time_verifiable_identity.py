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


class OneTimeVerifiableIdentityBase(VerifiableIdentityBase):
    pass


class OneTimeVerifiableIdentityCreate(VerifiableIdentityCreate):
    pass


class OneTimeVerifiableIdentityUpdate(VerifiableIdentityUpdate):
    pass


class OneTimeVerifiableIdentityUpdateMe(VerifiableIdentityUpdateMe):
    pass


class OneTimeVerifiableIdentity(VerifiableIdentity):
    pass


class OneTimeVerifiableIdentityPublic(VerifiableIdentityPublic):
    pass


class OneTimeVerifiableIdentityPublicMe(VerifiableIdentityPublicMe):
    pass
