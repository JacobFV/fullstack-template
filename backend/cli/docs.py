# $ docs
# $ docs build
# $ docs deploy
# $ docs serve
# $ docs ? -- retraieves relavent docs
# Info group commands

import subprocess
import webbrowser
import typer
from cli.utils import CODE_DIR, REPO_DIR


async def docs():
    typer.echo("Showing documentation...")
    webbrowser.open("https://github.com/verifyhumans/gotcha-v2/tree/main/docs")


async def build():
    subprocess.run(
        ["poetry", "run", "make", "html"],
        cwd=REPO_DIR,
        capture_output=False,
    )


async def deploy(build: bool = typer.Option(True)):
    if build:
        build()

    # deploy
    typer.
    raise NotImplemented("TODO: deploy ./build/html to the server")


async def serve(port: int = 8000, host: str = "0.0.0.0"):
    subprocess.run(
        [
            "poetry",
            "run",
            "sphinx-autobuild",
            "source",
            "build",
            "--port",
            port,
            "--host",
            host,
        ],
        cwd=REPO_DIR,
        capture_output=False,
    )


async def code():
    typer.echo("Showing code...")
    webbrowser.open("https://github.com/verifyhumans/gotcha-v2")
