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
# from app.schema.user.developer import Developer, DeveloperRead
from app.schema.system.api_key import APIKey as APIKey, APIKeyRead as APIKeyRead
from app.utils.crud import build_crud_endpoints


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


crud_router = build_crud_endpoints(
    t_model_base=APIKeyUseBase,
    t_model_read=APIKeyUseRead,
    t_model_in_db=APIKeyUse,
)
