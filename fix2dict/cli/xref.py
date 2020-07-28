import click
import json

from . import cli
from .utils.json import read_json, DEFAULT_INDENT


@cli.command("xref")
@click.argument("old", nargs=1, type=click.Path(exists=True))
@click.argument("new", nargs=1, type=click.Path(exists=True))
def xref(old, new):
    """
    Solve discrepancies between data by cross-reference.
    """
    old_filename = old
    new_filename = new
    old = read_json(old)
    new = read_json(new)
    for kind in [
        "abbreviations",
        "datatypes",
        "fields",
        "components",
        "messages",
    ]:

        def log(op, key):
            return print("-- New [{}] diff for kind {}: {}".format(op, kind, key))

        for (key, value) in new[kind].items():
            if key not in old[kind]:
                log(" ADDED ", key)
                value["history"]["added"] = new["version"]
            elif old[kind][key] != value:
                log("UPDATED", key)
                value["history"]["updated"] = new["version"]
        for (key, value) in old[kind].items():
            if key not in new[kind]:
                log("REMOVED", key)
                old[kind][key]["history"]["removed"] = new["version"]
    with open(old_filename, "w") as f:
        json.dump(old, f, indent=DEFAULT_INDENT)
    print("-- Written to '{}'".format(old_filename))
    with open(new_filename, "w") as f:
        json.dump(new, f, indent=DEFAULT_INDENT)
    print("-- Written to '{}'".format(new_filename))
