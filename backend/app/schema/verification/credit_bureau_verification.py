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
from app.schema.verification.verification import (
    Verification,
    VerificationBase,
    VerificationRead,
    VerificationUpdate,
)
from app.utils.crud import build_crud_endpoints


class CreditBureauVerificationBase(VerificationBase):
    pass


class CreditBureauVerificationRequest(
    CreditBureauVerificationBase, VerificationRequestBase
):
    pass


class CreditBureauVerificationRead(CreditBureauVerificationBase, VerificationRead):
    pass


class CreditBureauVerificationUpdate(CreditBureauVerificationBase, VerificationUpdate):
    pass


class CreditBureauVerification(CreditBureauVerificationBase, Verification):
    pass


crud_router = build_crud_endpoints(
    t_model_base=CreditBureauVerificationBase,
    t_model_create=CreditBureauVerificationRequest,
    t_model_read=CreditBureauVerificationRead,
    t_model_update=CreditBureauVerificationUpdate,
    t_model_in_db=CreditBureauVerification,
)
