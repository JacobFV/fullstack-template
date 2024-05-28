from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from functools import cached_property
from typing import Callable, ClassVar, Literal, Optional
import warnings
from pydantic import BaseModel

# from .user import User

from pydantic.config import ConfigDict
from sqlalchemy import Column, String, func, Index, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlmodel import Field, Relationship, Session, SQLModel, delete, select
from typing_extensions import Unpack

from app.core.redis import get_redis_connection
from app.utils.context import Context
from app.utils.errors import UnauthorizedUpdateError


from typing import Protocol, runtime_checkable


@runtime_checkable
class Privileges(Protocol):
    def __call__(self, *args, **kwargs) -> bool: ...


@runtime_checkable
class CreatePrivileges(Protocol):
    def __call__(self, model_create: ModelCreate, context: Context) -> bool: ...


@runtime_checkable
class ReadPrivileges(Protocol):
    def __call__(self, model_read: ModelRead, context: Context) -> bool: ...


@runtime_checkable
class UpdatePrivileges(Protocol):
    def __call__(
        self, model_update: ModelUpdate, model_in_db: ModelInDB, context: Context
    ) -> bool: ...


@runtime_checkable
class DeletePrivileges(Protocol):
    def __call__(self, model_in_db: ModelInDB, context: Context) -> bool: ...


def nobody_can_do(model: "ModelBase", /, *args, context: Context, **kwargs) -> bool:
    return False


def authenticated_can_do(
    model: "ModelBase", /, *args, context: Context, **kwargs
) -> bool:
    return context.user is not None


def public_can_do(model: "ModelBase", /, *args, context: Context, **kwargs) -> bool:
    return True


nobody_can_create: CreatePrivileges = nobody_can_do
authenticated_can_create: CreatePrivileges = authenticated_can_do
public_can_create: CreatePrivileges = public_can_do
nobody_can_read: ReadPrivileges = nobody_can_do
authenticated_can_read: ReadPrivileges = authenticated_can_do
public_can_read: ReadPrivileges = public_can_do
nobody_can_update: UpdatePrivileges = nobody_can_do
authenticated_can_update: UpdatePrivileges = authenticated_can_do
public_can_update: UpdatePrivileges = public_can_do
nobody_can_delete: DeletePrivileges = nobody_can_do
authenticated_can_delete: DeletePrivileges = authenticated_can_do
public_can_delete: DeletePrivileges = public_can_do


class ModelBase(SQLModel):

    ModelCreate: ClassVar[type[ModelCreate]]
    ModelUpdate: ClassVar[type[ModelUpdate]]
    ModelRead: ClassVar[type[ModelRead]]
    ModelInDB: ClassVar[type[ModelInDB]]


class ModelCreate(ModelBase):
    discriminator: str = Field(discriminator="type")
    OBJECT_CREATE_PRIVILEGES: ClassVar[CreatePrivileges] = nobody_can_create


class HasPrivileges(BaseModel, ABC):

    async def apply_privileges(self, context: Context):
        import asyncio

        async def check_and_set_privilege(k):
            privilege_fn = getattr(
                k, self.PRIVILEGES_FIELD_KEY, self.DEFAULT_FIELD_PRIVILEGES
            )
            if not await privilege_fn(self, context):
                setattr(self, k, None)

        tasks = [check_and_set_privilege(k) for k in self.model_fields]
        await asyncio.gather(*tasks)

    PRIVILEGES_FIELD_KEY: ClassVar[str]
    DEFAULT_FIELD_PRIVILEGES: ClassVar[Privileges] = nobody_can_do

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        cls.PRIVILEGES_FIELD_KEY = f"{cls.__name__}_privileges"


class ModelRead(HasPrivileges, ModelBase):

    id: int
    type: str = Field(discriminator="type")

    PRIVILEGES_FIELD_KEY: ClassVar[str] = "read_privileges"
    DEFAULT_FIELD_PRIVILEGES: ClassVar[ReadPrivileges] = public_can_read
    OBJECT_READ_PRIVILEGES: ClassVar[ReadPrivileges] = public_can_read


class ModelUpdate(HasPrivileges, ModelBase):

    type: str = Field(discriminator="type", exclude=True)

    PRIVILEGES_KEY: ClassVar[str] = "update_privileges"
    DEFAULT_FIELD_PRIVILEGES: ClassVar[UpdatePrivileges] = nobody_can_update
    OBJECT_UPDATE_PRIVILEGES: ClassVar[UpdatePrivileges] = nobody_can_update


class ModelInDB(ModelBase, table=True):
    __tablename__ = "entity"
    __mapper_args__ = {
        "polymorphic_identity": "entity",  # base class identity
        "polymorphic_on": "type",  # specifying which field is the discriminator
    }
    id: int = Field(autoincrement=True, primary_key=True, frozen=True)
    type: str = Field(nullable=False, index=True, frozen=True)

    OBJECT_DELETE_PRIVILEGES: ClassVar[DeletePrivileges] = nobody_can_delete

    def __init_subclass__(cls, **kwargs):
        tablename = cls.__tablename__ or cls.__name__.lower()
        mapper_args = getattr(cls, "__mapper_args__", {})
        mapper_args.update({"polymorphic_identity": tablename})
        setattr(cls, "__mapper_args__", mapper_args)
        return super().__init_subclass__(**kwargs)

    @classmethod
    def get_ddl(cls) -> str:
        # TODO: add constraints and security if applicable to all classes
        return ""

    @staticmethod
    def manually_run_all_ddl(session: Session):
        for subclass in ModelInDB.__subclasses__():
            session.execute(subclass.get_ddl())

    @classmethod
    def from_create(
        cls,
        model_create: ModelCreate,
        context: "Context",
        extra_keys: Optional[dict] = None,
        commit=True,
        refresh=True,
    ) -> ModelInDB:
        if commit is False and refresh is True:
            warnings.warn(
                "You have requested a refresh without making any commits. "
                "This may not be what you want if you are expecting the in-memory object to be up to date."
            )
        db_entity = cls(**model_create.model_dump(), **(extra_keys or {}))
        # subclasses wrap this and pass in extra keys needed for the indb model that are absent in the create model
        session = context.db_session
        session.add(db_entity)
        if commit:
            session.commit()
            if refresh:
                session.refresh(db_entity)
        session.commit()
        session.refresh(db_entity)
        return db_entity

    def update_from(
        self,
        model_update: ModelUpdate,
        context: "Context",
        extra_keys: Optional[dict] = None,
        commit=True,
        refresh=False,
    ) -> None:
        if commit is False and refresh is True:
            warnings.warn(
                "You have requested a refresh without making any commits. "
                "This may not be what you want if you are expecting the in-memory object to be up to date."
            )
        model_update = model_update.apply_privileges(model_update, context)
        self.update(
            {**model_update.model_dump(exclude_unset=True), **(extra_keys or {})}
        )
        if commit:
            context.db_session.commit()
            if refresh:
                context.db_session.refresh(self)

    def to_read(self, context: Context, refresh=False) -> ModelRead:
        if refresh:
            context.db_session.refresh(self)
        model_read = self.ModelRead.model_validate(self)
        model_read = model_read.apply_privileges(model_read, context)
        return model_read

    # active record methods
    def save(self, session: Session, refresh=False):
        session.add(self)
        session.commit()
        if refresh:
            session.refresh(self)

    def delete(self, session: Session, refresh=False):
        session.delete(self)
        session.commit()
        if refresh:
            session.refresh(self)

    @classmethod
    def find_by_id(cls, id: int, session: Session):
        sql = select(cls).where(cls.id == id)
        return session.exec(sql).first()

    @classmethod
    def find_all(cls, session: Session):
        sql = select(cls)
        return session.exec(sql).all()

    @classmethod
    def find_by_ids(cls, ids: list[int], session: Session):
        sql = select(cls).where(cls.id.in_(ids))
        return session.exec(sql).all()

    @classmethod
    def find_by_id_or_raise(cls, id: int, session: Session):
        entity = cls.find_by_id(id, session)
        if not entity:
            raise ValueError(f"Entity {id} not found")
        return entity

    @classmethod
    def update_by_id(
        cls,
        id: int,
        update_model: ModelUpdate,
        session: Session,
        commit=True,
        refresh=False,
    ):
        entity = cls.find_by_id_or_raise(id, session)
        entity.sqlmodel_update(update_model.model_dump(exclude_unset=True))
        if commit:
            session.commit()
            if refresh:
                session.refresh(entity)
        return entity

    @classmethod
    def update_by_ids(
        cls,
        ids: list[int],
        update_model: ModelUpdate,
        session: Session,
        commit=True,
        refresh=False,
    ):
        entities = cls.find_by_ids(ids, session)
        for entity in entities:
            updated_entity = entity.update(
                update_model.model_dump(exclude_unset=True), commit=False, refresh=False
            )
            session.add(updated_entity)
        if commit:
            session.commit()
            if refresh:
                for entity in entities:
                    session.refresh(entity)

    @classmethod
    def delete_by_id(cls, id: int, session: Session, commit=True):
        entity = cls.find_by_id_or_raise(id, session)
        entity.delete(session)
        if commit:
            session.commit()

    @classmethod
    def delete_by_ids(cls, ids: list[int], session: Session, commit=True):
        for id in ids:
            cls.delete_by_id(id, session, commit=False)
        if commit:
            session.commit()

    @classmethod
    def delete_all(cls, session: Session, commit=True):
        sql = delete(cls)
        session.exec(sql)
        if commit:
            session.commit()

    @classmethod
    def count(cls, session: Session):
        sql = select(func.count()).select_from(cls)
        return session.exec(sql).scalar()

    @classmethod
    def exists(cls, id: int, session: Session):
        return cls.find_by_id(id, session) is not None

    @classmethod
    def exists_by_ids(cls, ids: list[int], session: Session):
        return len(cls.find_by_ids(ids, session)) == len(ids)

    @classmethod
    def exists_all(cls, ids: list[int], session: Session):
        return cls.exists_by_ids(ids, session)

    @classmethod
    def exists_any(cls, ids: list[int], session: Session):
        return cls.exists_by_ids(ids, session)

    @classmethod
    def exists_none(cls, ids: list[int], session: Session):
        return not cls.exists_by_ids(ids, session)
