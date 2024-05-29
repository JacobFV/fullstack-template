# $ docs
# $ docs build
# $ docs deploy
# $ docs serve
# $ docs ? -- retraieves relavent docs
# Info group commands
@info_cli.command()
def docs():
    typer.echo("Showing documentation...")
    webbrowser.open("https://github.com/verifyhumans/gotcha-v2/tree/main/docs")


@info_cli.command()
def code():
    typer.echo("Showing code...")
    webbrowser.open("https://github.com/verifyhumans/gotcha-v2")
@dev_cli.command()
async def build_docs():
    code_dir = await get_settings().code_dir
    subprocess.run(
        ["poetry", "run", "make", "html"],
        cwd=code_dir,
        capture_output=False,
    )