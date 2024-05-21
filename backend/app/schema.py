from __future__ import annotations

from sqlmodel import Field, Relationship, Session


class SQLModelBase(SQLModel):
    pass


class SQLModelCreate(SQLModelBase):
    pass


class SQLModelUpdate(SQLModelBase):
    pass


class SQLModelInDB(SQLModelBase, table=True):
    @classmethod
    def init_ddl(cls, session: Session):
        pass


class SQLModelPublic(SQLModelBase):
    pass


class VerifiableIdentityBase(SQLModelBase):
    pass


class VerifiableIdentityCreate(VerifiableIdentityBase, SQLModelCreate):
    pass


class VerifiableIdentityUpdate(VerifiableIdentityBase, SQLModelUpdate):
    pass


class VerifiableIdentityUpdateMe(VerifiableIdentityBase, SQLModelUpdate):
    pass


class VerifiableIdentity(VerifiableIdentityBase, SQLModelInDB):
    id: int | None = Field(default=None, primary_key=True)


class VerifiableIdentityPublic(VerifiableIdentityBase, SQLModelPublic):
    id: int


class VerifiableIdentityPublicMe(VerifiableIdentityBase, SQLModelPublic):
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
class UserRegister(SQLModelBase):
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


class UpdatePassword(SQLModelBase):
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


class UsersPublic(SQLModelBase):
    data: list[UserPublic]
    count: int


# Verifier
class UserThatRequestsVerificationBase(UserBase):
    pass


class UserThatRequestsVerificationCreate(UserCreate):
    pass


class UserThatRequestsVerificationUpdate(UserUpdate):
    pass


class UserThatRequestsVerificationUpdateMe(UserUpdateMe):
    pass


class UserThatRequestsVerification(User):
    verification_requests: list[VerificationRequest] = Relationship(
        back_populates="verification_requested_by"
    )


class UserThatRequestsVerificationPublic(UserPublic):
    pass


class UserThatRequestsVerificationPublicMe(UserPublicMe):
    pass


# Shared properties
class ItemBase(SQLModelBase):
    title: str
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase, SQLModelCreate):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase, SQLModelUpdate):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, SQLModelInDB):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase, SQLModelPublic):
    id: int
    owner_id: int


class ItemsPublic(SQLModelBase):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModelBase):
    message: str


# JSON payload containing access token
class Token(SQLModelBase):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModelBase):
    sub: int | None = None


class NewPassword(SQLModelBase):
    token: str
    new_password: str


class VerificationRequestBase(SQLModelBase):
    verification_requested_by_id: int
    verification_requested_by: UserThatRequestsVerification
    who_to_verify_id: int
    who_to_verify: User


class VerificationRequestCreate(VerificationRequestBase, SQLModelCreate):
    pass


class VerificationRequestUpdate(VerificationRequestBase, SQLModelUpdate):
    pass


class VerificationRequest(VerificationRequestBase, SQLModelInDB):
    pass


class VerificationRequestPublic(VerificationRequestBase, SQLModelPublic):
    pass
