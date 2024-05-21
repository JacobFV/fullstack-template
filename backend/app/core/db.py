from sqlmodel import SQLModel, Session, create_engine, select

from app import crud
from app.core.config import get_settings, settings
from app.schema import User, UserCreate
from app.core.state import ApplicationState

connect_args = {"check_same_thread": False}
engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=True,
    connect_args=connect_args,
)


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-template/issues/28


async def init_db(session: Session, seed_if_new=False) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    SQLModel.metadata.create_all(engine)

    if seed_if_new:
        settings = await get_settings()
        if not settings.seeded_on:
            await seed_db(session)


async def seed_db(session: Session) -> None:

    crud.create_user(
        session=session,
        user_create=UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        ),
    )
