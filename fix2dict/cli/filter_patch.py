import click
import json
import jsonpatch

from .utils.json import read_json, DEFAULT_INDENT
from . import cli


def op_refers_to_docs(op):
    return "/docs/" in op["path"] or op["path"].endswith("\docs")


@cli.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
def filter_patch(src):
    patch = read_json(src)
    data = [op for op in patch if not op_refers_to_docs(op)]
    print(json.dumps(data, indent=DEFAULT_INDENT))
