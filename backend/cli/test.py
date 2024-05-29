import typer

test_cli = typer.Typer()

def test(test_name: str=None):
    subprocess.run(
        ["tests_start.sh"],
        cwd='code_dir',
        capture_output=False,
    )

async def coverage():
    bash = r"""\
        set -e
        set -x

        coverage run --source=app -m pytest
        coverage report --show-missing
        coverage html --title "${@-coverage}"
        """
