from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from enum import Enum
from functools import cached_property
from typing import ClassVar, Optional

from pydantic.config import ConfigDict
from sqlalchemy import Column, String, func
from sqlalchemy.ext.hybrid import hybrid_column
from sqlmodel import Field, Relationship, Session, SQLModel, delete, select
from typing_extensions import Unpack

from app.core.redis import get_redis_connection


class ModelBase(SQLModel):

    ModelCreate: ClassVar[type[ModelCreate]]
    ModelUpdate: ClassVar[type[ModelUpdate]]
    ModelRead: ClassVar[type[ModelRead]]
    ModelInDB: ClassVar[type[ModelInDB]]


class ModelCreate(ModelBase):
    pass


class ModelUpdate(ModelBase):
    class UpdatePrivileges(Enum):
        owner = "owner"
        authenticated = "authenticated"
        public = "public"

        def apply_privileges(self, model: ModelUpdate, model_owner_id, user_id):
            is_owner = model_owner_id == user_id
            is_authenticated = user_id is not None
            is_public = True

            for k in model.model_fields:
                match getattr(k, "update_privileges", None):
                    case ModelUpdate.UpdatePrivileges.owner:
                        if not is_owner:
                            setattr(model, k, None)
                    case ModelUpdate.UpdatePrivileges.authenticated:
                        if not is_authenticated:
                            setattr(model, k, None)
                    case ModelUpdate.UpdatePrivileges.public:
                        if not is_public:
                            setattr(model, k, None)
                    case _:
                        pass

            return model

    pass


class ModelRead(ModelBase):
    class ViewPrivileges(Enum):
        owner = "owner"
        authenticated = "authenticated"
        public = "public"

        def apply_privileges(self, model: ModelRead, model_owner_id, user_id):
            is_owner = model_owner_id == user_id
            is_authenticated = user_id is not None
            is_public = True

            for k in model.model_fields:
                match getattr(k, "view_privileges", None):
                    case ModelRead.ViewPrivileges.owner:
                        if not is_owner:
                            setattr(model, k, None)
                    case ModelRead.ViewPrivileges.authenticated:
                        if not is_authenticated:
                            setattr(model, k, None)
                    case ModelRead.ViewPrivileges.public:
                        if not is_public:
                            setattr(model, k, None)
                    case _:
                        pass

    pass


class ModelInDB(ModelBase, table=True):
    __tablename__ = "crud_object"
    __mapper_args__ = {
        "polymorphic_identity": "crud_object",  # base class identity
        "polymorphic_on": type,  # specifying which field is the discriminator
    }
    type: str = Field(sa_column=Column(String), index=True, nullable=False)

    def __init_subclass__(cls, **kwargs):
        tablename = cls.__tablename__ or cls.__name__.lower()
        mapper_args = getattr(cls, "__mapper_args__", {})
        mapper_args.update({"polymorphic_identity": tablename})
        setattr(cls, "__mapper_args__", mapper_args)
        return super().__init_subclass__(**kwargs)

    @classmethod
    @abstractmethod
    def get_ddl(cls) -> str:
        # TODO: add constraints and security if applicable to all classes
        pass

    @staticmethod
    def manually_run_all_ddl(session: Session):
        for subclass in ModelInDB.__subclasses__():
            session.execute(subclass.get_ddl())

    @classmethod
    def from_create(
        cls,
        create_model: ModelCreate,
        session: Session,
        user: User | None = None,
        extra_keys: Optional[dict] = None,
    ) -> ModelInDB:
        db_entity = cls(**create_model.model_dump(), **(extra_keys or {}))
        # subclasses wrap this and pass in extra keys needed for the indb model that are absent in the create model
        session.add(db_entity)
        session.commit()
        return db_entity

    def update_from(
        self,
        update_model: ModelUpdate,
        session: Session,
        user: User | None = None,
    ) -> None:
        self.sqlmodel_update(update_model.model_dump(exclude_unset=True))
        session.commit()

    def to_read(self, user: User | None = None) -> ModelRead:
        return self.ModelRead.model_validate(self)

    # active record methods
    def save(self, session: Session):
        session.add(self)
        session.commit()

    def delete(self, session: Session):
        session.delete(self)
        session.commit()

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
    ):
        entity = cls.find_by_id_or_raise(id, session)
        entity.sqlmodel_update(update_model.model_dump(exclude_unset=True))
        if commit:
            session.commit()
        return entity

    @classmethod
    def update_by_ids(
        cls,
        ids: list[int],
        update_model: ModelUpdate,
        session: Session,
        commit=True,
    ):
        entities = cls.find_by_ids(ids, session)
        for entity in entities:
            updated_entity = entity.update(
                update_model.model_dump(exclude_unset=True), commit=False
            )
            session.add(updated_entity)
        if commit:
            session.commit()

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
