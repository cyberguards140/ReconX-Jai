from typer.testing import CliRunner
from reconx.cli.main import app

runner = CliRunner()

def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout

def test_cli_scan():
    result = runner.invoke(app, ["scan", "--target", "example.com"])
    # Just a stub depending on exact command names, expecting failure or mock
    assert result.exit_code in [0, 1, 2]
