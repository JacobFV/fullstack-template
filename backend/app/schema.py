from __future__ import annotations

from sqlmodel import Field, Relationship, SQLModel, Session


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


class VerifiableIdentityBase(SQLModel):
    pass


class VerifiableIdentityCreate(VerifiableIdentityBase):
    pass


class VerifiableIdentityUpdate(VerifiableIdentityBase):
    pass


class VerifiableIdentityUpdateMe(VerifiableIdentityBase):
    pass


class VerifiableIdentity(VerifiableIdentityBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class VerifiableIdentityPublic(VerifiableIdentityBase):
    id: int


class VerifiableIdentityPublicMe(VerifiableIdentityBase):
    id: int


class OneTimeVerifiableIdentityBase(VerifiableIdentityBase):
    pass


class OneTimeVerifiableIdentityCreate(VerifiableIdentityCreate):
    pass


class OneTimeVerifiableIdentityUpdate(VerifiableIdentityUpdate):
    pass


class OneTimeVerifiableIdentityUpdateMe(VerifiableIdentityUpdateMe):
    pass


class OneTimeVerifiableIdentity(VerifiableIdentity, table=True):
    pass


class OneTimeVerifiableIdentityPublic(VerifiableIdentityPublic):
    pass


class OneTimeVerifiableIdentityPublicMe(VerifiableIdentityPublicMe):
    pass


# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(VerifiableIdentityBase, SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class UserCreate(VerifiableIdentityCreate, UserBase):
    password: str


# TODO replace email str with EmailStr when sqlmodel supports it
class UserRegister(SQLModel):
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


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(VerifiableIdentity, UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserPublic(VerifiableIdentityPublic, UserBase):
    id: int


class UserPublicMe(VerifiableIdentityPublicMe, UserBase):
    id: int


class UsersPublic(SQLModel):
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


class UserThatRequestsVerification(User, table=True):
    verification_requests: list[VerificationRequest] = Relationship(
        back_populates="verification_requested_by"
    )


class UserThatRequestsVerificationPublic(UserPublic):
    pass


class UserThatRequestsVerificationPublicMe(UserPublicMe):
    pass


# Shared properties
class ItemBase(SQLModel):
    title: str
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str


class VerificationRequestBase(SQLModel):
    verification_requested_by_id: int
    verification_requested_by: UserThatRequestsVerification
    who_to_verify_id: int
    who_to_verify: User


class VerificationRequestCreate(VerificationRequestBase):
    pass


class VerificationRequestUpdate(VerificationRequestBase):
    pass


class VerificationRequest(VerificationRequestBase):
    pass


class VerificationRequestPublic(VerificationRequestBase):
    pass
