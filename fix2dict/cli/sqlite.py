import click
import sqlite3
from sqlite3 import Error
import os

from . import cli
from ..sqlite import dict_to_mem_sqlite
from .utils.json import read_json

@cli.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
@click.argument("target", nargs=1, type=click.Path(exists=False))
def sqlite(src, target):
    """
    Transform FIX2dict JSON into SQLite data.
    """
    data = read_json(src)
    try:
        os.remove(target)
    except OSError:
        pass
    conn = None
    try:
        conn = sqlite3.connect(target)
    except Error as e:
        print(e)
    dict_to_mem_sqlite(data, conn)