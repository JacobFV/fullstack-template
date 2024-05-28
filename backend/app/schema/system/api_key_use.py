from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Optional

from sqlmodel import Field, Relationship
from app.schema.base import (
    DeletePrivileges,
    ModelBase,
    ModelCreate,
    ModelRead,
    ModelUpdate,
    ModelInDB,
    ReadPrivileges,
    nobody_can_delete,
)
from app.schema.system.billing import Money
from app.schema.system.api_key import APIKey as APIKey, APIKeyRead as APIKeyRead
from app.schema.user.ownership import owner_can_read
from app.utils.context import Context
from app.utils.crud import build_crud_endpoints


class APIKeyUseBase(ModelBase):
    pass


class APIKeyUseRead(APIKeyUseBase, ModelRead):
    api_key_id: int = Field()
    api_key: APIKeyRead = Field()
    timestamp: datetime = Field()
    ip_address: str = Field()
    user_agent: str = Field()
    http_headers: dict[str, str] = Field()
    http_path: str = Field()
    http_method: str = Field()

    OBJECT_READ_PRIVILEGES: ClassVar[ReadPrivileges] = owner_can_read


class APIKeyUse(APIKeyUseBase, ModelInDB):
    api_key_id: int = Field()
    api_key: APIKey = Field()
    timestamp: datetime = Field()
    ip_address: str = Field()
    user_agent: str = Field()
    http_headers: dict[str, str] = Field()
    http_path: str = Field()
    http_method: str = Field()

    @classmethod
    def from_create(
        cls,
        model_create: APIKeyUseCreate,
        context: "Context",
        extra_keys: Optional[dict] = None,
        commit=True,
        refresh=True,
    ) -> APIKeyUse:
        api_key_use_in_db = super().from_create(
            model_create=model_create,
            context=context,
            extra_keys=extra_keys,
            commit=commit,
            refresh=refresh,
        )
        return api_key_use_in_db

    OBJECT_DELETE_PRIVILEGES: ClassVar[DeletePrivileges] = nobody_can_delete

    def update_from(
        self,
        model_update: APIKeyUseUpdate,
        context: Context,
        extra_keys: dict | None = None,
        commit=True,
        refresh=False,
    ) -> None:
        return super().update_from(model_update, context, extra_keys, commit, refresh)

    def to_read(self, context: Context, refresh=False) -> APIKeyUseRead:
        return super().to_read(context, refresh=refresh)


crud_router = build_crud_endpoints(
    t_model_base=APIKeyUseBase,
    t_model_read=APIKeyUseRead,
    t_model_in_db=APIKeyUse,
)
