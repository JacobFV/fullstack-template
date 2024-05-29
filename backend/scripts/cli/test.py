
@dev_cli.command()
async def test():
    settings = await get_settings()
    code_dir = settings.code_dir
    subprocess.run(
        ["tests_start.sh"],
        cwd=code_dir,
        capture_output=False,
    )