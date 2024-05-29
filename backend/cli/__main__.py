cli = typer.Typer()

cli.add_typer(dev_cli, name="dev")
cli.add_typer(test_cli, name="test")
cli.add_typer(db_cli, name="db")
cli.add_typer(docs_cli, name="docs")
cli.add_typer(info_cli, name="info")

