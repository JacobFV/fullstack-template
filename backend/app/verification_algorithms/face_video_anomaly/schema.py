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
from app.verification_algorithms.base.schema import (
    Verification,
    VerificationBase,
    VerificationRead,
    VerificationCreate,
    VerificationUpdate,
)
from app.utils.crud import build_crud_endpoints
from app.schema.base import ModelRead


class FaceVideoAnomalyVerificationBase(VerificationBase):
    model_name: str = "face_video_anomaly_verification-001"


class FaceVideoAnomalyVerificationRequest(
    FaceVideoAnomalyVerificationBase, VerificationCreate
):
    pass


class FaceVideoAnomalyVerificationRead(
    FaceVideoAnomalyVerificationBase, VerificationRead
):
    model_name: str = Field(
        "face_video_anomaly_verification-001",
        schema_extra={"view_privileges": ModelRead.Privileges.owner},
    )


class FaceVideoAnomalyVerificationUpdate(
    FaceVideoAnomalyVerificationBase, VerificationUpdate
):
    pass


class FaceVideoAnomalyVerification(Verification):
    pass


crud_router = build_crud_endpoints(
    t_model_base=FaceVideoAnomalyVerificationBase,
    t_model_create=FaceVideoAnomalyVerificationRequest,
    t_model_read=FaceVideoAnomalyVerificationRead,
    t_model_update=FaceVideoAnomalyVerificationUpdate,
    t_model_in_db=FaceVideoAnomalyVerification,
)
