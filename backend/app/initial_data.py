import logging

from sqlmodel import Session

from app.core.db import engine, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def seed():
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


# keeping name `main` for compat
def main() -> None:
    seed()


if __name__ == "__main__":
    main()
