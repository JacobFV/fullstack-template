from __future__ import annotations

from abc import ABC
from typing import Any, ClassVar, Optional

from sqlmodel import Field, Relationship

from app.schema.base import (
    CreatePrivileges,
    DeletePrivileges,
    ModelBase,
    ModelCreate,
    ModelRead,
    ModelUpdate,
    ModelInDB,
    ReadPrivileges,
    UpdatePrivileges,
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
    owner_id: Identity.ID


class HasOwnerCreate(ModelCreate, HasOwnerBase):
    owner_id: Identity.ID

    OBJECT_CREATE_PRIVILEGES: ClassVar[CreatePrivileges] = owner_can_create


class HasOwnerRead(ModelRead, HasOwnerBase):
    owner_id: Identity.ID = Field(
        schema_extras={ModelRead.PRIVILEGES_KEY: None}
    )  # TODO: implement default field authorization

    DEFAULT_FIELD_PRIVILEGES: ClassVar[ReadPrivileges] = owner_can_read


class HasOwnerUpdate(ModelUpdate, HasOwnerBase):
    owner_id: Identity.ID = Field(schema_extras={ModelUpdate.PRIVILEGES_KEY: nobody_can_do})

    DEFAULT_FIELD_PRIVILEGES: ClassVar[UpdatePrivileges] = owner_can_update


class HasOwner(ModelInDB, HasOwnerBase):
    owner_id: ID = Field(foreign_key="owner.id")
    owner: Identity = Relationship(back_populates="owned_items")

    @classmethod
    def from_create(
        cls,
        model_create: HasOwnerCreate,
        context: "Context",
        extra_keys: Optional[dict] = None,
        commit=True,
        refresh=True,
    ) -> HasOwner:
        has_owner_in_db = super().from_create(
            model_create=model_create,
            context=context,
            extra_keys=extra_keys,
            commit=commit,
            refresh=refresh,
        )
        return has_owner_in_db

    def update_from(
        self,
        model_update: HasOwnerUpdate,
        context: Context,
        extra_keys: dict | None = None,
        commit=True,
        refresh=False,
    ) -> None:
        return super().update_from(
            model_update=model_update,
            context=context,
            extra_keys=extra_keys,
            commit=commit,
            refresh=refresh,
        )

    def to_read(self, context: Context, refresh=False) -> HasOwnerRead:
        return super().to_read(context, refresh=refresh)

    OBJECT_DELETE_PRIVILEGES: ClassVar[DeletePrivileges] = owner_can_delete
