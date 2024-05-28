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
    CreatePrivileges,
    DeletePrivileges,
    ModelBase,
    ModelCreate,
    ModelInDB,
    ModelRead,
    ModelUpdate,
    ReadPrivileges,
    UpdatePrivileges,
)

from app.schema.user.ownership import (
    owner_can_create,
    owner_can_delete,
    owner_can_read,
    owner_can_update,
    HasOwner,
    HasOwnerBase,
    HasOwnerCreate,
    HasOwnerRead,
    HasOwnerUpdate,
)

# from app.schema.verification.verification import Verification, VerificationRead
from app.utils.crud import build_crud_endpoints


class IdentityBase(HasOwnerBase, IdentityBase, ModelBase):
    image_bytes: Optional[bytes] = Field()


class IdentityCreate(IdentityBase, HasOwnerCreate, ModelCreate):
    image_bytes: Optional[bytes] = Field()
    owner_id: int | None

    CREATE_PRIVILEGES: ClassVar[CreatePrivileges] = owner_can_create


class IdentityRead(IdentityBase, HasOwnerRead, ModelRead):
    image_bytes: Optional[bytes] = Field()
    verifications_performed_ids: list[int] = Field()
    owned_items: list["HasOwnerRead"] = Field(
        schema_extra={ModelRead.PRIVILEGES_KEY: owner_can_read}
    )

    READ_PRIVILEGES: ClassVar[ReadPrivileges] = owner_can_read


class IdentityUpdate(IdentityBase, HasOwnerUpdate, ModelUpdate):
    image_bytes: Optional[bytes] = Field()

    DEFAULT_FIELD_PRIVILEGES: ClassVar[UpdatePrivileges] = owner_can_update
    OBJECT_UPDATE_PRIVILEGES: ClassVar[UpdatePrivileges] = owner_can_update


class Identity(IdentityBase, HasOwner, ModelInDB, table=True):
    image_bytes: Optional[bytes] = Field()
    verifications_performed_ids: list[int] = Field(foreign_key="verification.id")
    verifications_performed: list["Verification"] = Relationship(
        back_populates="target"
    )
    owned_items: list["HasOwner"] = Relationship(backref="owner")

    OBJECT_DELETE_PRIVILEGES: ClassVar[DeletePrivileges] = owner_can_delete

    @classmethod
    def from_create(
        cls,
        model_create: IdentityCreate,
        session: Session,
        user: "User" | None = None,
        extra_keys: Optional[dict] = None,
    ) -> ModelInDB:
        model_in_db: Identity = super().from_create(
            model_create, session, user, extra_keys
        )
        model_in_db.save(session=session, refresh=True)
        model_in_db.owner_id = model_create.id
        return model_in_db


crud_router = build_crud_endpoints(
    t_model_base=IdentityBase,
    t_model_create=IdentityCreate,
    t_model_read=IdentityRead,
    t_model_update=IdentityUpdate,
    t_model_in_db=Identity,
)
