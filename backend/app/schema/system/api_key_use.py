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
from app.schema.system.api_key import APIKey as APIKey, APIKeyRead as APIKeyRead
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


class APIKeyUse(APIKeyUseBase, ModelInDB):
    api_key_id: int = Field()
    api_key: APIKey = Field()
    timestamp: datetime = Field()
    ip_address: str = Field()
    user_agent: str = Field()
    http_headers: dict[str, str] = Field()
    http_path: str = Field()
    http_method: str = Field()

    OBJECT_DELETE_PRIVILEGES: ClassVar[DeletePrivileges] = nobody_can_delete


crud_router = build_crud_endpoints(
    t_model_base=APIKeyUseBase,
    t_model_read=APIKeyUseRead,
    t_model_in_db=APIKeyUse,
)
