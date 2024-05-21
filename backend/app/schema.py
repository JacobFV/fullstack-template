from __future__ import annotations
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from functools import cached_property
from typing import ClassVar, Optional
from typing_extensions import Unpack
from app.core.redis import get_redis_connection
from pydantic.config import ConfigDict
from sqlalchemy import func
from sqlalchemy import Column, String

from sqlmodel import Field, Relationship, Session, SQLModel, select, delete


class CRUDBase(SQLModel):

    ModelCreate: ClassVar[type[CRUDCreate]]
    ModelUpdate: ClassVar[type[CRUDUpdate]]
    ModelRead: ClassVar[type[CRUDRead]]
    ModelInDB: ClassVar[type[CRUDInDB]]


class CRUDCreate(CRUDBase):
    pass


class CRUDUpdate(CRUDBase):
    pass


class CRUDInDB(CRUDBase, table=True):
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
        for subclass in CRUDInDB.__subclasses__():
            session.execute(subclass.get_ddl())

    @classmethod
    def from_create(cls, create_model: CRUDCreate, session: Session, **extra_keys):
        db_entity = cls(**create_model.model_dump(), **(extra_keys or {}))
        # subclasses wrap this and pass in extra keys needed for the indb model that are absent in the create model
        session.add(db_entity)
        session.commit()
        return db_entity

    @classmethod
    def update_from(cls, id: int, update_model: CRUDUpdate, session: Session):
        cls.update_by_id(id, update_model, session)

    @classmethod
    def to_read(cls, id: int, session: Session):
        db_entity = cls.find_by_id(id, session)
        return cls.ModelRead.model_validate(db_entity)

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
        update_model: CRUDUpdate,
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
        update_model: CRUDUpdate,
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


class CRUDRead(CRUDBase):
    pass


class VerifiableIdentityBase(CRUDBase):
    pass


class VerifiableIdentityCreate(VerifiableIdentityBase, CRUDCreate):
    image: Optional[bytes]


class VerifiableIdentityUpdate(VerifiableIdentityBase, CRUDUpdate):
    pass


class VerifiableIdentityUpdateMe(VerifiableIdentityBase, CRUDUpdate):
    pass


class VerifiableIdentity(VerifiableIdentityBase, CRUDInDB):
    id: int | None = Field(default=None, primary_key=True, autoincrement=True)
    image: Optional[bytes]


class VerifiableIdentityPublic(VerifiableIdentityBase, CRUDRead):
    id: int
    image: Optional[bytes]


class VerifiableIdentityPublicMe(VerifiableIdentityBase, CRUDRead):
    id: int


class OneTimeVerifiableIdentityBase(VerifiableIdentityBase):
    pass


class OneTimeVerifiableIdentityCreate(VerifiableIdentityCreate):
    pass


class OneTimeVerifiableIdentityUpdate(VerifiableIdentityUpdate):
    pass


class OneTimeVerifiableIdentityUpdateMe(VerifiableIdentityUpdateMe):
    pass


class OneTimeVerifiableIdentity(VerifiableIdentity):
    pass


class OneTimeVerifiableIdentityPublic(VerifiableIdentityPublic):
    pass


class OneTimeVerifiableIdentityPublicMe(VerifiableIdentityPublicMe):
    pass


# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(VerifiableIdentityBase):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class UserCreate(VerifiableIdentityCreate, UserBase):
    password: str


# TODO replace email str with EmailStr when sqlmodel supports it
class UserRegister(CRUDBase):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(VerifiableIdentityUpdate, UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(VerifiableIdentityUpdateMe, UserBase):
    full_name: str | None = None
    email: str | None = None


class UpdatePassword(CRUDBase):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(VerifiableIdentity, UserBase):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserPublic(VerifiableIdentityPublic, UserBase):
    id: int


class UserPublicMe(VerifiableIdentityPublicMe, UserBase):
    id: int


class UsersPublic(CRUDBase):
    data: list[UserPublic]
    count: int


# Verifier
class UserThatRequestsVerificationBase(UserBase):
    pass


class UserThatRequestsVerificationCreate(UserCreate):
    stripe_user_access_token: str | None = None


class UserThatRequestsVerificationUpdate(UserUpdate):
    pass


class UserThatRequestsVerificationUpdateMe(UserUpdateMe):
    stripe_user_access_token: str | None = None


class UserThatRequestsVerification(User):
    verification_requests: list[Verification] = Relationship(
        back_populates="verification_requested_by"
    )
    stripe_user_access_token: str | None = None


class UserThatRequestsVerificationPublic(UserPublic):
    pass


class UserThatRequestsVerificationPublicMe(UserPublicMe):
    verification_requests: list[Verification]


# Shared properties
class ItemBase(CRUDBase):
    title: str
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase, CRUDCreate):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase, CRUDUpdate):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, CRUDInDB):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase, CRUDRead):
    id: int
    owner_id: int


class ItemsPublic(CRUDBase):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(CRUDBase):
    message: str


# JSON payload containing access token
class Token(CRUDBase):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(CRUDBase):
    sub: int | None = None


class NewPassword(CRUDBase):
    token: str
    new_password: str


class VerificationStatus(Enum):
    REQUESTED = "requested"
    IN_PROGRESS = "in_progress"
    VERIFIED = "verified"
    FAILED = "failed"


class VerificationBase(CRUDBase):
    pass


# TODO: change on_completion_webhook_url and on_completion_redirect_url to URLStr when sqlmodel supports it
class VerificationRequestBase(VerificationBase, CRUDCreate):
    who_to_verify_id: int
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None


class HasReddisChannel(CRUDInDB):

    @hybrid_column
    def redis_channel_name(self):
        return f"redis_{self.__class__.__name__.lower()}_{self.id}"

    @redis_channel_name.expression
    def redis_channel_name(cls):
        from sqlalchemy import func

        return func.concat("redis_", func.lower(cls.__name__), "_", cls.id)

    async def publish_message(self, message: str):
        connection = await get_redis_connection()
        await connection.publish(self.redis_channel_name, message)

    @cached_property
    async def redis_channel_listener(self):
        connection = await get_redis_connection()
        pubsub = connection.pubsub()
        await pubsub.subscribe(self.redis_channel_name)
        return pubsub

    async def listen_for_messages(self, message_handler):
        async for message in self.redis_channel_listener.listen():
            if message["type"] == "message":
                await message_handler(message["data"])


class Verification(HasReddisChannel, VerificationBase, CRUDInDB):
    verification_requested_by_id: int
    verification_requested_by: UserThatRequestsVerification
    who_to_verify_id: int
    who_to_verify: User
    verf_status: VerificationStatus
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None


class VerificationPublic(VerificationBase, CRUDRead):
    verification_requested_by_id: int
    verification_requested_by: UserThatRequestsVerification
    who_to_verify_id: int
    who_to_verify: User
    verf_status: VerificationStatus
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None


class FaceVideoAnomalyVerificationBase(VerificationBase):
    model_name: str = "face_video_anomaly_verification-001"


class FaceVideoAnomalyVerificationRequest(
    FaceVideoAnomalyVerificationBase, VerificationRequestBase
):
    pass


class FaceVideoAnomalyVerification(Verification):
    pass


class FaceVideoAnomalyVerificationPublic(
    FaceVideoAnomalyVerificationBase, VerificationPublic
):
    pass


class FaceImageMatchVerificationBase(VerificationBase):
    algorithm_name: str = "face_image_match_verification-001"


class FaceImageMatchVerification(FaceImageMatchVerificationBase, Verification):
    additional_provided_face_images: list[bytes] | None = None

    @hybrid_property
    def all_provided_face_images(self):
        return self.additional_provided_face_images + [self.who_to_verify.image]

    @all_provided_face_images.expression
    def all_provided_face_images(cls):
        return func.array_cat(
            cls.additional_provided_face_images, func.array([cls.who_to_verify.image])
        )


class FaceImageMatchVerificationPublic(
    FaceImageMatchVerificationBase, VerificationPublic
):
    pass


class HandSignVerificationBase(VerificationBase):
    model_name: str = "hand_sign_verification-001"


class HandSignVerification(HandSignVerificationBase, Verification):
    hand_letters: list[str]


class HandSignVerificationPublic(HandSignVerificationBase, VerificationPublic):
    pass


class LivingPupilVerificationBase(VerificationBase):
    model_name: str = "living_pupil_verification-001"


class LivingPupilVerification(LivingPupilVerificationBase, Verification):
    pass


class LivingPupilVerificationPublic(LivingPupilVerificationBase, VerificationPublic):
    pass


class HumanSpeechVerificationBase(VerificationBase):
    model_name: str = "human_speech_verification-001"


class HumanSpeechVerification(HumanSpeechVerificationBase, Verification):
    pass


class HumanSpeechVerificationPublic(HumanSpeechVerificationBase, VerificationPublic):
    pass


class CreditBureauVerificationBase(VerificationBase):
    pass


class CreditBureauVerification(CreditBureauVerificationBase, Verification):
    pass


class CreditBureauVerificationPublic(CreditBureauVerificationBase, VerificationPublic):
    pass


class ProofOfIDVerificationBase(VerificationBase):
    pass


class ProofOfIDVerification(ProofOfIDVerificationBase, Verification):
    pass


class ProofOfIDVerificationPublic(ProofOfIDVerificationBase, VerificationPublic):
    pass
