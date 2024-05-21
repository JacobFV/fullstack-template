from sqlmodel import Session
import typer

# DB group commands
from app.core import config
from app.core.db import drop_db, init_db, seed_db, test_connect_db, engine

# Assuming engine is created from a configuration setting

db_cli = typer.Typer()


@db_cli.command()
async def drop(
    confirm: bool = typer.Option(
        False, "--confirm", prompt="Are you sure you want to drop the database?"
    )
):
    if confirm:
        typer.echo("Dropping database...")
        with Session(engine) as session:
            await drop_db(session)
        typer.echo("Database dropped.")
    else:
        typer.echo("Database drop cancelled.")


@db_cli.command()
def init():
    typer.echo("Initializing database...")
    with Session(engine) as session:
        init_db(session)
    typer.echo("Database initialized.")


@db_cli.command()
def seed(test: bool = typer.Option(False, "--test")):
    typer.echo("Seeding database...")
    with Session(engine) as session:
        seed_db(session)
    typer.echo("Database seeded.")


@db_cli.command()
def alembic(*args):
    typer.echo("Running alembic command...")
    import subprocess

    subprocess.run(
        ["alembic", *args],
        check=True,
    )
    typer.echo("Alembic command completed.")


@db_cli.command()
def test_connect():
    typer.echo("Testing database connection...")
    with Session(engine) as session:
        test_connect_db(session)
    typer.echo("Database connection tested.")


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
