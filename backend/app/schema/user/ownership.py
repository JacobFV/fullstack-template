from __future__ import annotations

from abc import ABC
from typing import Any, Optional

from sqlmodel import Field, Relationship

from app.schema.base import (
    ModelBase,
    ModelCreate,
    ModelRead,
    ModelUpdate,
    ModelInDB,
    nobody_can_do,
)
from app.schema.id import ID
from app.schema.user.identity import (
    IdentityBase,
    IdentityCreate,
    IdentityRead,
    IdentityUpdate,
)
from app.utils.context import Context

if TYPE_CHECKING:
    from app.schema.user.developer import (
        DeveloperBase,
        DeveloperCreate,
        DeveloperRead,
        DeveloperUpdate,
        Developer,
    )
    from app.schema.user.identity import (
        IdentityBase,
        IdentityCreate,
        IdentityRead,
        IdentityUpdate,
        Identity,
    )


def owner_can_do(base_model: "HasOwnerBase", /, *, context: Context) -> bool:
    return context.user.id == base_model.owner_id


def owner_can_create(create_model: "HasOwnerCreate", /, *, context: Context) -> bool:
    return context.user.id == create_model.owner_id


def owner_can_read(read_model: "HasOwnerRead", /, *, context: Context) -> bool:
    return context.user.id == read_model.owner_id


def owner_can_update(
    update_model: "HasOwnerUpdate", db_model: "HasOwner", /, *, context: Context
) -> bool:
    return context.user.id == db_model.owner_id


def owner_can_delete(db_model: "HasOwner", /, *, context: Context) -> bool:
    return context.user.id == db_model.owner_id


class HasOwnerBase(ABC):
    owner_id: int


class HasOwnerCreate(ModelCreate, HasOwnerBase):
    owner_id: int


class HasOwnerRead(ModelRead, HasOwnerBase):
    owner_id: int = Field(
        schema_extras={ModelRead.PRIVILEGES_KEY: None}
    )  # TODO: implement default field autorization


class HasOwnerUpdate(ModelUpdate, HasOwnerBase):
    owner_id: int = Field(schema_extras={ModelUpdate.PRIVILEGES_KEY: nobody_can_do})


class HasOwner(ModelInDB, HasOwnerBase):
    owner_id: ID = Field(foreign_key="owner.id")
    owner: Identity = Relationship(back_populates="owned_items")
