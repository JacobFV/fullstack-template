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
def seed():
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
