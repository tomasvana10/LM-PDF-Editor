import subprocess
from pathlib import Path
from typing import Literal

import typer

from .settings import get_settings

app = typer.Typer()
this_dir = Path(__file__).resolve().parent
settings = get_settings()


def fastapi_run(op: Literal["run"] | Literal["dev"]):
    return subprocess.run(
        [
            "fastapi",
            op,
            this_dir / "server",
            "--host",
            settings["api_host"],
            "--port",
            str(settings["api_port"]),
        ]
    )


@app.command()
def deploy():
    return fastapi_run("run")


@app.command()
def dev():
    return fastapi_run("dev")


app()
