from __future__ import annotations

from datetime import datetime

from sqlmodel import Field, Relationship
from app.schema.base import (
    ModelBase,
    ModelCreate,
    ModelRead,
    ModelUpdate,
    ModelInDB,
)

from app.schema.system.billing import Money
from app.schema.system.auth_scope import AuthScope
from app.schema.user.developer import Developer, DeveloperRead
from app.utils.crud import build_crud_endpoints


class APIKeyBase(ModelBase):
    pass


class APIKeyCreate(APIKeyBase, ModelCreate):
    name: str
    description: str
    spend_limit: Money.T
    scopes: list[str]
    expires_at: datetime


class APIKeyRead(APIKeyBase, ModelRead):
    name: str = Field()
    description: str = Field()
    owner_id: int = Field()
    owner: DeveloperRead = Field(exclude=True)
    spend_limit: Money.T = Field()
    scopes: list[AuthScope] = Field()
    expires_at: datetime = Field()
    truncated_secret: str = Field()
    uses: list["APIKeyUseRead"] = Field(exclude=True)


class APIKeyUpdate(APIKeyBase, ModelUpdate):
    description: str = Field()
    spend_limit: Money.T = Field()


class APIKey(APIKeyBase, ModelInDB):
    name: str = Field()
    description: str = Field()
    created_at: datetime = Field()
    expires_at: datetime = Field()
    owner_id: int = Field(foreign_key="developer.id")
    owner: Developer = Relationship(back_populates="api_keys")
    scopes: list[str] = Field()
    uses: list["APIKeyUse"] = Relationship(back_populates="api_key")
    spend_limit: Money.T = Field()
    secret: str = Field(private=True, exclude=True)


crud_router = build_crud_endpoints(
    t_model_base=APIKeyBase,
    t_model_create=APIKeyCreate,
    t_model_read=APIKeyRead,
    t_model_update=APIKeyUpdate,
    t_model_in_db=APIKey,
)
