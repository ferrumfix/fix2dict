import click

from fix2dict.cli import cli
from fix2dict.cli.utils.xml import read_xml_root
from fix2dict.cli.utils.json import beautify_json
from fix2dict.extension_pack import ExtensionPack


@cli.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
def convert_ep(src):
    """
    Convert Expansion Pack files from one format to another.

    <SRC> must be a valid XML file containing the definition of an Extension
    Pack. The resulting JSON Patch will be printed.
    """
    root = read_xml_root("", src, opt=False)[0]
    patch = ExtensionPack(root).to_jsonpatch().to_string()
    print(beautify_json(patch))
