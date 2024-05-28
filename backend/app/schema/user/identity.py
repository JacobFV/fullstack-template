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

from app.schema.base import (
    ModelBase,
    ModelCreate,
    ModelInDB,
    ModelRead,
    ModelUpdate,
)

# from app.schema.verification.verification import Verification, VerificationRead
from app.utils.crud import build_crud_endpoints


class IdentityBase(ModelBase):
    pass


class IdentityCreate(IdentityBase, ModelCreate):
    image_bytes: Optional[bytes] = Field()


class IdentityRead(IdentityBase, ModelRead):
    image_bytes: Optional[bytes] = Field()
    verifications_performed_ids: list[int] = Field()


class IdentityUpdate(IdentityBase, ModelUpdate):
    pass


class Identity(IdentityBase, ModelInDB, table=True):
    image_bytes: Optional[bytes] = Field()
    verifications_performed_ids: list[int] = Field(foreign_key="verification.id")
    verifications_performed: list["Verification"] = Relationship(
        back_populates="target"
    )


crud_router = build_crud_endpoints(
    t_model_base=IdentityBase,
    t_model_create=IdentityCreate,
    t_model_read=IdentityRead,
    t_model_update=IdentityUpdate,
    t_model_in_db=Identity,
)
