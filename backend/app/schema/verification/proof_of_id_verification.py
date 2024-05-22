from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from enum import Enum
from functools import cached_property
from typing import ClassVar, Optional

from pydantic.config import ConfigDict
from sqlalchemy import Column, String, func
from sqlmodel import Field, Relationship, Session, SQLModel, delete, select
from typing_extensions import Unpack

from app.core.redis import get_redis_connection


class ProofOfIDVerificationBase(VerificationBase):
    pass


class ProofOfIDVerification(ProofOfIDVerificationBase, Verification):
    pass


class ProofOfIDVerificationPublic(ProofOfIDVerificationBase, VerificationPublic):
    pass
