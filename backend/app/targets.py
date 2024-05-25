import os
import subprocess
import webbrowser
from datetime import datetime

import typer
import uvicorn

from app.core import logger
from app.core.config import settings
from app.core.db import create_db_and_tables, get_db, init_db, seed_db
from app.__main__ import fastapi_app

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
info_cli = typer.Typer()
db_cli = typer.Typer()
dev_cli = typer.Typer()

# Adding sub-command groups to the main CLI
cli.add_typer(info_cli, name="info")
cli.add_typer(db_cli, name="db")
cli.add_typer(dev_cli, name="dev")


# Main command: serve
@cli.command()
def serve(host: str = settings.HOST, port: int = settings.PORT):
    uvicorn.run(fastapi_app, host=host, port=port)


# Info group commands
@info_cli.command()
def docs():
    typer.echo("Showing documentation...")
    webbrowser.open("https://github.com/verifyhumans/gotcha-v2/tree/main/docs")


@info_cli.command()
def code():
    typer.echo("Showing code...")
    webbrowser.open("https://github.com/verifyhumans/gotcha-v2")


@info_cli.command()
def status():
    if settings.ENVIRONMENT == "production":
        typer.echo("Running on production. Checking container health...")
        # Implement your container health check logic here
        # This could be a script that checks Docker container statuses, for example:
        os.system("docker ps --filter 'health=healthy'")
    else:
        typer.echo("Not running in production environment.")


@info_cli.command()
def logs(days: int = 1):
    typer.echo(f"Fetching logs for the last {days} days.")
    typer.echo("Streaming logs (press Ctrl+C to stop)...")
    try:
        subprocess.run(["tail", "-f", settings.LOG_FILE])
    except KeyboardInterrupt:
        typer.echo("Stopped streaming logs.")


# DB group commands
@db_cli.command()
def drop(
    confirm: bool = typer.Option(
        False, "--confirm", prompt="Are you sure you want to drop the database?"
    )
):
    if confirm:
        typer.echo("Dropping database...")
        with get_db() as db:
            db.execute(f"DROP DATABASE IF EXISTS {settings.POSTGRES_DB}")
        typer.echo("Database dropped.")
    else:
        typer.echo("Database drop cancelled.")


@db_cli.command()
def init(session=typer.Depends(get_db)):
    typer.echo("Initializing database...")
    init_db(session)
    typer.echo("Database initialized.")


@db_cli.command()
def seed(session=typer.Depends(get_db)):
    typer.echo("Seeding database...")
    seed_db(session)


@db_cli.command()
def backup():
    typer.echo("Backing up database...")
    raise NotImplementedError("Not implemented yet")

    db = get_db()
    import os
    import shutil
    from datetime import datetime

    backup_dir = settings.BACKUP_DIR
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = os.path.join(backup_dir, f"db_backup_{timestamp}.sql")

    command = f"pg_dump -h {settings.POSTGRES_SERVER} -p {settings.POSTGRES_PORT} -U {settings.POSTGRES_USER} -d {settings.POSTGRES_DB} -f {backup_file}"
    os.system(command)

    # Optionally, compress the backup file
    shutil.make_archive(backup_file, "zip", backup_dir, backup_file)
    typer.echo("Database backed up.")


@db_cli.command()
def restore():
    typer.echo("Restoring database from backup...")
    raise NotImplementedError("Not implemented yet")

    import os
    from datetime import datetime
    import shutil
    from sqlmodel import Session

    backup_dir = settings.BACKUP_DIR
    latest_backup = max(
        [
            os.path.join(backup_dir, f)
            for f in os.listdir(backup_dir)
            if f.endswith(".sql.zip")
        ],
        default=None,
        key=os.path.getctime,
    )

    if latest_backup:
        typer.echo(f"Restoring from {latest_backup}...")
        # Unzip the backup file
        with zipfile.ZipFile(latest_backup, "r") as zip_ref:
            zip_ref.extractall(backup_dir)

        # Get the SQL file name from the zip file
        sql_file = latest_backup.replace(".zip", "")

        # Restore the database from the SQL file
        command = f"psql -h {settings.POSTGRES_SERVER} -p {settings.POSTGRES_PORT} -U {settings.POSTGRES_USER} -d {settings.POSTGRES_DB} -f {sql_file}"
        os.system(command)

        # Clean up extracted files
        os.remove(sql_file)
        typer.echo("Database restored from backup.")
    else:
        typer.echo("No backup file found.")


@db_cli.command()
def migrate():
    typer.echo("Migrating database...")

    # TODO: use the alembic scripts
    raise NotImplementedError("Not implemented yet")


# Dev group commands
@dev_cli.command()
def test():
    typer.echo("Running tests...")
    raise NotImplementedError("Not implemented yet")


@dev_cli.command()
def generate_docs():
    typer.echo("Generating docs...")
    raise NotImplementedError("Not implemented yet")


@dev_cli.command()
def deploy(environment: str):
    typer.echo(f"Deploying to {environment}...")
    raise NotImplementedError("Not implemented yet")


@dev_cli.command()
def build():
    typer.echo("Building project...")
    raise NotImplementedError("Not implemented yet")


if __name__ == "__main__":
    cli()
