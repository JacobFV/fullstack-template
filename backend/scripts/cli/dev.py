# Main command: serve
@dev_cli.command()
async def serve(host: str = Settings.HOST, port: int = Settings.PORT):
    uvicorn.run(fastapi_app, host=host, port=port)


@cli.command()
def dev(
    host: str = typer.Option(
        default=settings.DEV_HOST,
        help="Host to run the server on.",
    ),
    port: int = typer.Option(
        default=settings.DEV_PORT,
        help="Port to run the server on.",
    ),
    new_db: bool = typer.Option(
        default=False,
        help="Create a new database.",
    ),
):
    with Session(engine) as db_session:
        with typer.progressbar(
            length=5, label="Processing database and server operations"
        ) as progress:
            dev_cli_endpoints.test()
            progress.update(1)
            db_cli_endpoints.test_connect()
            progress.update(1)
            if new_db:
                db_cli_endpoints.drop_db(db_session)
                progress.update(1)
                db_cli_endpoints.init_db(db_session)
                progress.update(1)
                db_cli_endpoints.seed_db(db_session)
                progress.update(1)
            else:
                progress.update(3)
            dev_cli_endpoints.serve(host, port)
