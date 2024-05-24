import os
import subprocess
from typing import Annotated
import typer
import uvicorn

from app.core.config import Settings, get_settings
from app.main import fastapi_app

dev_cli = typer.Typer()

SettingsTyperDep = Annotated[Settings, typer.Depends(get_settings)]


# Main command: serve
@dev_cli.command()
async def serve(host: str = Settings.HOST, port: int = Settings.PORT):
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
async def test():
    settings = await get_settings()
    code_dir = settings.code_dir
    subprocess.run(
        ["tests_start.sh"],
        cwd=code_dir,
        capture_output=False,
    )


@dev_cli.command()
async def deploy(environment: str):
    import semver
    import git

    settings = await get_settings()
    repo_dir = typer.get_app_dir(
        settings.app_name
    )  # Use settings.app_name instead of hardcoded string
    repo = git.Repo(repo_dir)

    # Ensure we are on the prod branch and it's up to date
    repo.git.checkout("prod")
    repo.git.pull("origin", "prod")

    # Merge current branch into prod
    current_branch = repo.active_branch.name
    repo.git.merge(current_branch)

    # Increment the patch version
    new_version = semver.VersionInfo.parse(settings.version).bump_patch()
    settings.version = str(new_version)  # Update the settings version

    # Commit the version change
    repo.index.add(["settings.py"])  # Assuming version is stored in settings.py
    repo.index.commit(f"Bump version to {new_version}")

    # Push changes to prod
    repo.git.push("origin", "prod")

    # Create a new GitHub release
    typer.echo(f"Creating a new GitHub release for version {new_version}")
    subprocess.run(
        [
            "gh",
            "release",
            "create",
            str(new_version),
            "--notes",
            "Auto-generated release",
        ],
        cwd=repo_dir,
        capture_output=False,
    )

    typer.echo(f"Deploying to {environment}...")
    # Assuming a GitHub workflow handles the deployment when changes are pushed to prod    # Assuming a GitHub workflow handles the deployment when changes are pushed to prod    # Assuming a GitHub workflow handles the deployment when changes are pushed to prod


@dev_cli.command()
def build():
    typer.echo("Building project...")
    raise NotImplementedError("Not implemented yet")
