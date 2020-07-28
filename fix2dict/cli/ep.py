import click

from . import cli
from .utils.xml import read_xml_root
from .utils.json import beautify_json
from ..extension_pack import ExtensionPack


@cli.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
def ep(src):
    """
    Transform an XML-formatted EP file into a JSON Patch.

    <SRC> must be a valid XML file containing the definition of an Extension
    Pack. The resulting JSON Patch will be printed.
    """
    root = read_xml_root("", src, opt=False)[0]
    patch = ExtensionPack(root).to_jsonpatch().to_string()
    print(beautify_json(patch))
