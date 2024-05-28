from __future__ import annotations

from datetime import datetime, timedelta
from functools import cached_property
from typing import TYPE_CHECKING, ClassVar
from pydantic import computed_field

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
)

from app.schema.system.billing import Money
from app.schema.system.auth_scope import AuthScope
from app.schema.user.developer import Developer, DeveloperRead
from app.schema.user.ownership import (
    HasOwner,
    HasOwnerCreate,
    HasOwnerRead,
    HasOwnerUpdate,
    owner_can_create,
    owner_can_delete,
    owner_can_read,
    owner_can_update,
)
from app.utils.crud import build_crud_endpoints


if TYPE_CHECKING:
    from app.schema.user.developer import Developer, DeveloperRead
    from app.schema.system.api_key_use import APIKeyUse, APIKeyUseRead


class APIKeyBase(ModelBase):
    pass


class APIKeyCreate(APIKeyBase, HasOwnerCreate, ModelCreate):
    name: str
    description: str
    spend_limit: Money.T
    scopes: list[str]
    expires_at: datetime

    OBJECT_CREATE_PRIVILEGES: ClassVar[CreatePrivileges] = owner_can_create


class APIKeyRead(APIKeyBase, HasOwnerRead, ModelRead):
    name: str = Field()
    description: str = Field()
    owner_id: int = Field()
    spend_limit: Money.T = Field()
    scopes: list[AuthScope] = Field()
    expires_at: datetime = Field()
    truncated_secret: str = Field()
    uses: list["APIKeyUseRead"] = Field()  # yes, nested models here

    OBJECT_READ_PRIVILEGES: ClassVar[ReadPrivileges] = owner_can_read


class APIKeyUpdate(APIKeyBase, HasOwnerUpdate, ModelUpdate):
    description: str = Field()
    spend_limit: Money.T = Field()

    DEFAULT_FIELD_PRIVILEGES: ClassVar[UpdatePrivileges] = owner_can_update
    OBJECT_UPDATE_PRIVILEGES: ClassVar[UpdatePrivileges] = owner_can_update


class APIKey(APIKeyBase, HasOwner, ModelInDB):
    name: str = Field()
    description: str = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expiration: timedelta = Field(frozen=True)

    @computed_field
    @cached_property
    def expires_at(self) -> datetime:
        return self.created_at + self.expiration

    owner_id: int = Field(foreign_key="developer.id")
    owner: Developer = Relationship(back_populates="api_keys")
    scopes: list[str] = Field()
    uses: list["APIKeyUse"] = Relationship(back_populates="api_key")
    spend_limit: Money.T = Field()
    secret_key: str = Field(frozen=True, exclude=True)

    OBJECT_DELETE_PRIVILEGES: ClassVar[DeletePrivileges] = owner_can_delete


crud_router = build_crud_endpoints(
    t_model_base=APIKeyBase,
    t_model_create=APIKeyCreate,
    t_model_read=APIKeyRead,
    t_model_update=APIKeyUpdate,
    t_model_in_db=APIKey,
)
