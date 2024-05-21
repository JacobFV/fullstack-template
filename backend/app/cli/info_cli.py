import webbrowser
import typer

info_cli = typer.Typer()


# Info group commands
@info_cli.command()
def docs():
    typer.echo("Showing documentation...")
    webbrowser.open("https://github.com/verifyhumans/gotcha-v2/tree/main/docs")


@info_cli.command()
def code():
    typer.echo("Showing code...")
    webbrowser.open("https://github.com/verifyhumans/gotcha-v2")
