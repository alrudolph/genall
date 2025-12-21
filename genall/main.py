from pathlib import Path

import click

from .genall import GenAll
from .filters.file_filter import ConfigFileFilter

@click.command()
@click.option(
    "--path",
    prompt="Path to the base directory",
    help="The base directory path.",
)
def main(path: str) -> None:
    base_path = Path(path).expanduser().resolve()
    #
    # TODO: path could just be file
    #
    ga = GenAll(base_path)
    ga.write_to_file(ConfigFileFilter.from_file(base_path / ".genall.yaml"))
