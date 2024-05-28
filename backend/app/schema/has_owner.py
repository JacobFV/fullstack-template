from abc import ABC
from typing import Any

from app.schema.base import ModelBase, ModelRead, ModelUpdate
from app.utils.context import Context


class HasOwnerBase(ABC):
    pass


class HasOwnerCreate(HasOwnerBase):
    owner: Any


class HasOwnerUpdate(HasOwnerBase):
    owner: Any


class HasOwnerRead(HasOwnerBase):
    owner: Any


class HasOwner(HasOwnerBase):
    owner: Any


def owner_can_do(base_model: HasOwnerBase, /, *, context: Context) -> bool:
    return context.user.id == base_model.owner_id


def owner_can_read(read_model: ModelRead, /, *, context: Context) -> bool:
    return context.user.id == read_model.owner_id


def owner_can_update(
    update_model: ModelUpdate, db_model: HasOwner, /, *, context: Context
) -> bool:
    return context.user.id == db_model.owner_id
