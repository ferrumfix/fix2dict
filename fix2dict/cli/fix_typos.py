import click
import json
import jsonpatch

from ..utils import read_json, DEFAULT_INDENT
from . import cli


@cli.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
@click.argument("typos-path", nargs=1, type=click.Path(exists=True))
def fix_typos(src, typos_path):
    pass
