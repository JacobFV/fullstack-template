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


class ProofOfIDVerificationBase(VerificationBase):
    pass


class ProofOfIDVerificationRequest(ProofOfIDVerificationBase, VerificationCreate):
    pass


class ProofOfIDVerificationRead(ProofOfIDVerificationBase, VerificationRead):
    pass


class ProofOfIDVerificationUpdate(ProofOfIDVerificationBase, VerificationUpdate):
    pass


class ProofOfIDVerification(ProofOfIDVerificationBase, Verification):
    pass


crud_router = build_crud_endpoints(
    t_model_base=ProofOfIDVerificationBase,
    t_model_create=ProofOfIDVerificationRequest,
    t_model_read=ProofOfIDVerificationRead,
    t_model_update=ProofOfIDVerificationUpdate,
    t_model_in_db=ProofOfIDVerification,
)
