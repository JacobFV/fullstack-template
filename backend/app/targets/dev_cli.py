import os
import subprocess
from typing import Annotated
import typer

from app.core.config import Settings, get_settings
from app.main import fastapi_app

dev_cli = typer.Typer()

SettingsTyperDep = Annotated[Settings, typer.Depends(get_settings)]


# Main command: serve
@dev_cli.command()
async def serve(host: str = settings.HOST, port: int = settings.PORT):
    uvicorn.run(fastapi_app, host=host, port=port)


from app.core.config import get_settings


@dev_cli.command()
async def status():
    settings = await get_settings()
    if settings.ENVIRONMENT == "production":
        typer.echo("Running on production. Checking container health...")
        # Implement your container health check logic here
        # This could be a script that checks Docker container statuses, for example:
        os.system("docker ps --filter 'health=healthy'")
    else:
        typer.echo("Not running in production environment.")


@dev_cli.command()
async def logs(days: int = 1):
    typer.echo(f"Fetching logs for the last {days} days.")
    typer.echo("Streaming logs (press Ctrl+C to stop)...")
    settings = await get_settings()
    try:
        subprocess.run(["tail", "-f", settings.LOG_FILE])
    except KeyboardInterrupt:
        typer.echo("Stopped streaming logs.")


@dev_cli.command()
async def build_docs():
    code_dir = await get_settings().code_dir
    subprocess.run(
        ["poetry", "run", "make", "html"],
        cwd=code_dir,
        capture_output=False,
    )


@dev_cli.command()
async def run_tests():
    settings = await get_settings()
    code_dir = settings.code_dir
    subprocess.run(
        ["poetry", "run", "pytest", "--cov=app", "--cov-report=term-missing"],
        cwd=code_dir,
        capture_output=False,
    )
