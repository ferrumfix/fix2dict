import click
import json

from . import cli
from .utils.json import read_json
from ..schema import validate_v1


@cli.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
def validate(src):
    """
    Check a JSON file for correctness.
    """
    validate_v1(read_json(src))
