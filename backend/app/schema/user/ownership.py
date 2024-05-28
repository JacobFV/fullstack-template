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
from app.utils.context import Context


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


class OwnerBase(ModelBase):
    pass


class OwnerCreate(OwnerBase, ModelCreate):
    pass


class OwnerRead(OwnerBase, ModelRead):
    owned_items: list["HasOwnerRead"] = Field(
        schema_extra={ModelRead.PRIVILEGES_KEY: owner_can_read}
    )


class OwnerUpdate(OwnerBase, ModelUpdate):
    pass


class Owner(OwnerBase, ModelInDB, table=True):
    owned_items: list["HasOwner"] = Relationship(backref="owner")


class HasOwnerBase(ABC):
    owner_id: int


class HasOwnerCreate(ModelCreate, HasOwnerBase):
    owner_id: int


class HasOwnerRead(ModelRead, HasOwnerBase):
    owner_id: int = Field()


class HasOwnerUpdate(ModelUpdate, HasOwnerBase):
    owner_id: int = Field(schema_extras={ModelUpdate.PRIVILEGES_KEY: nobody_can_do})


class HasOwner(ModelInDB, HasOwnerBase):
    owner_id: ID = Field(foreign_key="owner.id")
    owner: Owner = Relationship(back_populates="owner")
