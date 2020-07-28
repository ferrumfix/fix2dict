import click

from . import cli
from .utils.json import read_json
from ..review import RepositoryReview


@cli.command()
@click.argument("repo", nargs=1, type=click.Path(exists=True))
def review(repo):
    """
    Print a short summary of a FIX2dict-produced JSON document.
    """
    repo = read_json(repo)
    print(RepositoryReview(repo))
