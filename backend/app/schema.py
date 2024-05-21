from __future__ import annotations
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from functools import cached_property
from typing import Optional
import aio_pika
from app.core.aoimq import get_aoimq_channel
from app.core.redis import get_redis_connection
from sqlalchemy import func

from sqlmodel import Field, Relationship, Session, SQLModel


class CRUDBase(SQLModel):
    pass


class CRUDCreate(CRUDBase):
    pass


class CRUDUpdate(CRUDBase):
    pass


class CRUDInDB(CRUDBase, table=True):

    @classmethod
    @abstractmethod
    def init_ddl(cls, session: Session):
        pass  # TODO: add constraints and security if applicable to all classes

    @staticmethod
    def init_all_ddl(session: Session):
        for subclass in CRUDInDB.__subclasses__():
            if hasattr(subclass, "init_ddl"):
                subclass.init_ddl(session)


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
    verification_requests: list[VerificationRequest] = Relationship(
        back_populates="verification_requested_by"
    )
    stripe_user_access_token: str | None = None


class UserThatRequestsVerificationPublic(UserPublic):
    pass


class UserThatRequestsVerificationPublicMe(UserPublicMe):
    verification_requests: list[VerificationRequest]


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


class VerificationRequestStatus(Enum):
    REQUESTED = "requested"
    IN_PROGRESS = "in_progress"
    VERIFIED = "verified"
    FAILED = "failed"


class VerificationRequestBase(CRUDBase):
    pass


# TODO: change on_completion_webhook_url and on_completion_redirect_url to URLStr when sqlmodel supports it
class VerificationRequestCreate(VerificationRequestBase, CRUDCreate):
    who_to_verify_id: int
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None


class VerificationRequestUpdate(VerificationRequestBase, CRUDUpdate):
    pass


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


class VerificationRequest(HasReddisChannel, VerificationRequestBase, CRUDInDB):
    verification_requested_by_id: int
    verification_requested_by: UserThatRequestsVerification
    who_to_verify_id: int
    who_to_verify: User
    verf_status: VerificationRequestStatus
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None


class FaceVideoAnomalyVerification(VerificationRequest):
    check_anomaly_in_face_video: bool = True

    model_name: str = "face_video_anomaly_verification-001"


class HandSignVerification(VerificationRequest):
    ask_to_make_hand_signs: bool = True
    hand_letters: list[str] | None = None

    model_name: str = "hand_sign_verification-001"


class FaceImageMatchVerification(VerificationRequest):
    check_match_against_provided_face_images: bool = True
    additional_provided_face_images: list[bytes] | None = None

    algorithm_name: str = "face_image_match_verification-001"

    @hybrid_property
    def all_provided_face_images(self):
        return self.additional_provided_face_images + [self.who_to_verify.image]

    @all_provided_face_images.expression
    def all_provided_face_images(cls):
        return func.array_cat(
            cls.additional_provided_face_images, func.array([cls.who_to_verify.image])
        )


class FingerprintVerification(VerificationRequest):
    check_fingerprint: bool = True


class VerificationRequestPublic(VerificationRequestBase, CRUDRead):
    verification_requested_by_id: int
    verification_requested_by: UserThatRequestsVerification
    who_to_verify_id: int
    who_to_verify: User
    verf_status: VerificationRequestStatus
    on_completion_webhook_url: str
    on_completion_redirect_url: str | None = None
