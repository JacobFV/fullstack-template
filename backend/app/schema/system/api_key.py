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
from app.schema.system.billing import Money
from app.schema.user.developer import Developer, DeveloperRead


class APIKeyBase(ModelBase):
    pass


class APIKeyRead(APIKeyBase, ModelRead):
    name: str
    description: str
    owner_id: int
    owner: DeveloperRead
    spend_limit: Money.T
    scopes: list[str]
    expires_at: datetime
    truncated_secret: str


class APIKeyCreate(APIKeyBase, ModelCreate):
    name: str
    description: str
    spend_limit: Money.T
    scopes: list[str]
    expires_at: datetime


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
    uses: list[APIKeyUse]
    spend_limit: Money.T
    secret: str = Field(private=True)


class APIKeyUseBase(ModelBase):
    pass


class APIKeyUseRead(APIKeyUseBase, ModelRead):
    api_key_id: int
    api_key: APIKeyRead
    timestamp: datetime
    ip_address: str
    user_agent: str
    headers: dict[str, str]
    path: str
    method: str


class APIKeyUse(APIKeyUseBase, ModelInDB):
    api_key_id: int
    api_key: APIKey
    timestamp: datetime
    ip_address: str
    user_agent: str
    headers: dict[str, str]
    path: str
    method: str
