from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session, select

from app.core import security
from app.core.config import settings
from app.core.db import engine
from backend.app.schema import TokenPayload, User, VerifiableIdentity

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_verifiable_identity(
    request: Request, session: SessionDep, token: TokenDep
) -> VerifiableIdentity:
    identity = _get_current_user(session, token, raise_on_not_found=False)
    if not identity:
        ghost_identity = request.headers.get("ghost_identity")
        identity = session.exec(select(User).where(User.id == ghost_identity)).first()
    return identity


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    return _get_current_user(session, token)


def _get_current_user(
    session: SessionDep, token: TokenDep, raise_on_not_found: bool = True
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        if raise_on_not_found:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            return None
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
