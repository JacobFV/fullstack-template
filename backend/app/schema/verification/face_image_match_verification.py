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


class FaceImageMatchVerificationBase(VerificationBase):
    algorithm_name: str = "face_image_match_verification-001"


class FaceImageMatchVerification(FaceImageMatchVerificationBase, Verification):
    additional_provided_face_images: list[bytes] | None = None

    @hybrid_property
    def all_provided_face_images(self):
        return self.additional_provided_face_images + [self.who_to_verify.image]

    @all_provided_face_images.expression
    def all_provided_face_images(cls):
        return func.array_cat(
            cls.additional_provided_face_images, func.array([cls.who_to_verify.image])
        )


class FaceImageMatchVerificationPublic(
    FaceImageMatchVerificationBase, VerificationPublic
):
    pass
