import typer
from datetime import datetime

cli = typer.Typer()

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
def serve(host: str = "127.0.0.1", port: int = 8000):
    typer.echo(f"Serving on http://{host}:{port}")


# Info group commands
@info_cli.command()
def docs():
    typer.echo("Showing documentation...")


@info_cli.command()
def code():
    typer.echo("Showing code...")


@info_cli.command()
def status():
    typer.echo("System status: All systems operational.")


@info_cli.command()
def logs(days: int = 1):
    typer.echo(f"Fetching logs for the last {days} days.")


# DB group commands
@db_cli.command()
def drop(
    confirm: bool = typer.Option(
        False, "--confirm", prompt="Are you sure you want to drop the database?"
    )
):
    if confirm:
        typer.echo("Dropping database...")
    else:
        typer.echo("Database drop cancelled.")


@db_cli.command()
def init():
    typer.echo("Initializing database...")


@db_cli.command()
def seed():
    typer.echo("Seeding database...")


@db_cli.command()
def backup():
    typer.echo("Backing up database...")


@db_cli.command()
def restore():
    typer.echo("Restoring database from backup...")


@db_cli.command()
def migrate():
    typer.echo("Migrating database...")


# Dev group commands
@dev_cli.command()
def test():
    typer.echo("Running tests...")


@dev_cli.command()
def deploy(environment: str):
    typer.echo(f"Deploying to {environment}...")


@dev_cli.command()
def build():
    typer.echo("Building project...")


if __name__ == "__main__":
    cli()
