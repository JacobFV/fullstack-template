from __future__ import annotations

from datetime import datetime

from sqlmodel import Field
from app.schema.base import (
    ModelBase,
    ModelCreate,
    ModelRead,
    ModelUpdate,
    ModelInDB,
)
from app.schema.system.api_key import APIKey as _APIKey, APIKeyRead as _APIKeyRead
from app.schema.system.billing import Money
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
    name: str
    description: str
    owner_id: int
    owner: DeveloperRead
    spend_limit: Money.T
    scopes: list[str]
    expires_at: datetime
    truncated_secret: str
    uses: list[APIKeyUseRead]


class APIKeyUpdate(APIKeyBase, ModelUpdate):
    description: str
    spend_limit: Money.T


class APIKey(APIKeyBase, ModelInDB):
    name: str
    description: str
    created_at: datetime
    expires_at: datetime
    owner_id: int
    owner: Developer
    scopes: list[str]
    uses: list["APIKeyUse"]
    spend_limit: Money.T
    secret: str = Field(private=True)


crud_router = build_crud_endpoints(
    t_model_base=APIKeyBase,
    t_model_create=APIKeyCreate,
    t_model_read=APIKeyRead,
    t_model_update=APIKeyUpdate,
    t_model_in_db=APIKey,
)
