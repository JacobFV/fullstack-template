from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from enum import Enum
from functools import cached_property
from typing import ClassVar, Optional
from pydantic import field_validator

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


class IdentityBase(HasOwnerBase, OwnerBase, ModelBase):
    image_bytes: Optional[bytes] = Field()


from app.schema.user.ownership import (
    HasOwner,
    HasOwnerBase,
    HasOwnerCreate,
    HasOwnerRead,
    HasOwnerUpdate,
    Owner,
    OwnerBase,
    OwnerCreate,
    OwnerRead,
    OwnerUpdate,
)


class IdentityCreate(IdentityBase, HasOwnerCreate, OwnerCreate, ModelCreate):
    image_bytes: Optional[bytes] = Field()

    owner_id: int | None


class IdentityRead(IdentityBase, HasOwnerRead, OwnerRead, ModelRead):
    image_bytes: Optional[bytes] = Field()
    verifications_performed_ids: list[int] = Field()


class IdentityUpdate(IdentityBase, HasOwnerUpdate, OwnerUpdate, ModelUpdate):
    image_bytes: Optional[bytes] = Field()


class Identity(IdentityBase, HasOwner, Owner, ModelInDB, table=True):
    image_bytes: Optional[bytes] = Field()
    verifications_performed_ids: list[int] = Field(foreign_key="verification.id")
    verifications_performed: list["Verification"] = Relationship(
        back_populates="target"
    )

    OBJECT_DELETE_PRIVILEGES: ClassVar[DeletePrivileges] = owner_can_delete

    @classmethod
    def from_create(
        cls,
        model_create: IdentityCreate,
        session: Session,
        user: "User" | None = None,
        extra_keys: Optional[dict] = None,
    ) -> ModelInDB:
        model_in_db = super().from_create(model_create, session, user, extra_keys)
        model_in_db.owner_id = model_create.id
        return model_in_db


crud_router = build_crud_endpoints(
    t_model_base=IdentityBase,
    t_model_create=IdentityCreate,
    t_model_read=IdentityRead,
    t_model_update=IdentityUpdate,
    t_model_in_db=Identity,
)
