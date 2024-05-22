import logging

from sqlmodel import SQLModel, Session, create_engine, select
from sqlalchemy import Engine
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.config import get_settings, settings
from app import crud
from app.schema.schema import User, UserCreate


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
    # from sqlmodel import SQLModel
    # We are using Alembic to create the tables
    # # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

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


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def test_connect_db() -> None:
    try:
        with Session(db_engine) as session:
            # Try to create session to check if DB is awake
            session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise e


async def drop_db(db_engine: Engine) -> None:
    settings = await get_settings()
    db_engine.execute(f"DROP DATABASE IF EXISTS {settings.POSTGRES_DB}")
