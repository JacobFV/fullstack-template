import os
import subprocess
import webbrowser
from datetime import datetime
from sqlmodel import Session

import typer
import uvicorn

from app.core import logger
from app.core.config import settings
from app.core.db import engine
from app.main import fastapi_app

cli = typer.Typer(
    """\
    # CLI Commands Documentation

    ## Main Commands
    - `serve`: Start the server on a specified host and port.

    ## Info Commands
    - `docs`: Show documentation.
    - `code`: Show codebase.
    - `status`: Check the status of the backend systems.
    - `logs`: Fetch logs for the specified number of days.

    ## Database Commands
    - `init`: Initialize the database.
    - `seed`: Seed the database with initial data.
    - `backup`: Backup the database.
    - `restore`: Restore the database from a backup.
    - `migrate`: Migrate the database schema.

    ## Development Commands
    - `test`: Run tests.
    - `deploy`: Deploy the application to a specified environment.
    - `build`: Build the project.
    """
)

# Sub-command groups
from app.cli.db_cli import db_cli
from app.cli.info_cli import info_cli
from app.cli.dev_cli import dev_cli
import app.cli.db_cli as db_cli_endpoints
import app.cli.info_cli as info_cli_endpoints
import app.cli.dev_cli as dev_cli_endpoints


# Adding sub-command groups to the main CLI
cli.add_typer(info_cli, name="info")
cli.add_typer(db_cli, name="db")
cli.add_typer(dev_cli, name="dev")


@cli.command()
def dev(
    host: str = typer.Option(
        default=settings.DEV_HOST,
        help="Host to run the server on.",
    ),
    port: int = typer.Option(
        default=settings.DEV_PORT,
        help="Port to run the server on.",
    ),
):
    with Session(engine) as db_session:
        with typer.progressbar(
            length=6, label="Processing database and server operations"
        ) as progress:
            db_cli_endpoints.test_connect()
            progress.update(1)
            dev_cli_endpoints.test()
            progress.update(1)
            db_cli_endpoints.drop_db(db_session)
            progress.update(1)
            db_cli_endpoints.init_db(db_session)
            progress.update(1)
            db_cli_endpoints.seed_db(db_session)
            progress.update(1)
            dev_cli_endpoints.serve(host, port)
            progress.update(1)


if __name__ == "__main__":
    cli()
