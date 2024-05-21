import typer

# DB group commands
from app.core import config
from app.core.db import seed_db, test_db


db_cli = typer.Typer()


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
def alembic(*args):
    typer.echo("Running alembic command...")
    import subprocess

    subprocess.run(
        ["alembic", *args],
        check=True,
    )
    typer.echo("Alembic command completed.")


@db_cli.command()
def test():
    test_db()
