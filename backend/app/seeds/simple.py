from sqlmodel import Session
from app.schema.user.user import User, UserCreate


async def seed_db(session: Session) -> None:

    crud.create_user(
        session=session,
        user_create=UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        ),
    )
