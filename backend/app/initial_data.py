import logging

from sqlmodel import Session

from app.core.db import engine, init_db, seed_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# keeping name `main` for compat
async def main() -> None:
    logger.info("Creating initial data")
    with Session(engine) as session:
        await init_db(session)
        await seed_db(session)
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
