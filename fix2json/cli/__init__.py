import json
import click
import jsonpatch

from fix2json.__version__ import __version__
from fix2json.extension_pack import ExtensionPack
from fix2json.fix_version import FixVersion
from fix2json.output_formats import (
    dict_to_mem_sqlite,
    transform_basic_repository_v1,
    transform_orchestra_v1,
    transform_unified_repository_v1,
)
from fix2json.patch import apply_patch
from fix2json.review import RepositoryReview
from fix2json.schema import fix2json_JSON_SCHEMA, validate_fix2json_json
from .utils.options import opt_patch
from .utils.xml import read_xml_root

DEFAULT_JSON_INDENT = 2


@click.group(name="FIX2json")
@click.version_option(__version__)
def cli():
    """
    Easy and effective tooling for manipulating FIX Repository data.
    """
    pass


@cli.command()
def schema():
    """
    Print the JSON Schema used by FIX2json.
    """
    click.echo(fix2json_JSON_SCHEMA)


@cli.command()
@click.argument("json-src", nargs=1, type=click.Path(exists=True))
def summary(json_src):
    """
    Print a short summary of a FIX2json document's contents.
    """
    repo = read_json(json_src)
    click.echo(RepositoryReview(repo))


@cli.command("jsonpatch")
@click.argument("json-src", nargs=1, type=click.Path(exists=True))
@click.argument("patch-src", nargs=1, type=click.Path(exists=True))
def patch(json_src, patch_src):
    """
    Apply the JSON Patch of an Expansion Pack to a FIX2json document.
    """
    patch = jsonpatch.JsonPatch(read_json(patch_src))
    data = read_json(json_src)
    data_patched = apply_patch(data, patch)
    click.echo(json.dumps(data_patched, indent=DEFAULT_JSON_INDENT))


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
        json.dump(old, f, indent=DEFAULT_JSON_INDENT)
    print("-- Written to '{}'".format(old_filename))
    with open(new_filename, "w") as f:
        json.dump(new, f, indent=DEFAULT_JSON_INDENT)
    print("-- Written to '{}'".format(new_filename))


@cli.command("convert-ep-to-jsonpatch")
@click.argument("src", nargs=1, type=click.Path(exists=True))
def convert_ep_to_jsonpatch(src):
    """
    Convert a XML Expansion Pack file into a JSON Patch.

    <SRC> must be a valid XML file containing the definition of an Extension
    Pack. The resulting JSON Patch will be printed.
    """
    root = read_xml_root("", src, opt=False)[0]
    patch = ExtensionPack(root).to_jsonpatch().to_string()
    click.echo(beautify_json(patch))


@cli.command("convert-json-to-sqlite")
@click.argument("src", nargs=-1, type=click.Path(exists=True))
@click.argument("target", nargs=-1, type=click.Path(exists=False))
def convert_json_to_sqlite(fmt, files):
    """
    Convert a FIX2json document to a SQLite database.
    """
    src = files[0]
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


@cli.command("convert-basic-to-json")
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def convert_basic_to_json(input_fmt, files):
    """
    Convert raw FIX "Basic" Repository data to a JSON file.
    """
    src = files[0]
    data = transform_basic_repository_v1(
        abbreviations=read_xml_root(src, "Abbreviations.xml"),
        categories=read_xml_root(src, "Categories.xml"),
        components=read_xml_root(src, "Components.xml"),
        datatypes=read_xml_root(src, "Datatypes.xml"),
        enums=read_xml_root(src, "Enums.xml", opt=False),
        fields=read_xml_root(src, "Fields.xml", opt=False),
        messages=read_xml_root(src, "Messages.xml", opt=False),
        msg_contents=read_xml_root(src, "MsgContents.xml", opt=False),
        sections=read_xml_root(src, "Sections.xml"),
    )
    data["meta"]["fix2json"]["md5"] = dirhash(src, "md5")
    validate_fix2json_json(data)
    click.echo(json.dumps(data, indent=DEFAULT_JSON_INDENT))


@cli.command("convert-unified-to-json")
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def convert_unified_to_json(input_fmt, files):
    """
    Convert raw FIX "Unified" Repository data to a JSON file.
    """
    src = files[0]
    root = read_xml_root("", src, opt=False)[8]
    phrases = read_xml_root("", phrases, opt=False)
    data = transform_unified_repository_v1(root, phrases)
    click.echo(json.dumps(data, indent=DEFAULT_JSON_INDENT))


@cli.command("convert-orchestra-to-json")
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def convert_orchestra_to_json(input_fmt, files):
    """
    Convert FIX Orchestra data to a JSON file.
    """
    src = files[0]
    root = read_xml_root("", src, opt=False)[8]
    phrases = read_xml_root("", phrases, opt=False)
    data = transform_unified_repository_v1(root, phrases)
    click.echo(json.dumps(data, indent=DEFAULT_JSON_INDENT))


@cli.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
def filter_patch(src):
    patch = read_json(src)
    data = [op for op in patch if not op_refers_to_docs(op)]
    click.echo(json.dumps(data, indent=DEFAULT_JSON_INDENT))


def op_refers_to_docs(op):
    return "/docs/" in op["path"] or op["path"].endswith("\docs")


def beautify_json(json_string: str):
    return json.dumps(json.loads(json_string), indent=DEFAULT_JSON_INDENT)


def read_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError:
        err("JSON")
