import click
import jsonpatch
import json

from . import cli
from .utils.xml import read_xml_root
from .utils.json import read_json, DEFAULT_INDENT
from ..repository import transform_orchestra_v1


@cli.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
def repo_o(src):
    """
    Transform FIX Orchestra data into JSON.

    The resulting data will feature:

    \b
    - High-quality Markdown documentation obtained from several sources, plus
      minor improvements, e.g.
      * links to ISO standards,
      * RFC 2119 terms capitalization,
      * links for internal navigation,
      * markup, bold text, etc.
    - Full breakdown into fields and components.
    - Information about included Extension Packs.
    - General cleanup and improved data consistency across all FIX protocol
      versions.

    <SRC> is a directory pointing to input FIX Repository data ("Basic"
    flavor only, "Intermediate" and "Unified" is not accepted). Specifically,
    FIX2dict will look for the following files inside <SRC>:

    \b
    - `Abbreviation.xml`
    - `Categories.xml`
    - `Components.xml`
    - `Datatypes.xml`
    - `Fields.xml`
    - `Sections.xml`
    - `Messages.xml`
    - `MsgContents.xml`

    Note: not all of these are mandatory. Future versions of FIX2dict might
    look for additional files.

    Output data is written to <DST>, which must be an existing directory.
    Filenames are properly generated according to FIX protocol version. Old
    files in <DST> might get overwritten WITHOUT BACKUP!
    """
    root = read_xml_root("", src, opt=False)
    data = transform_orchestra_v1(root)
    print(json.dumps(data, indent=DEFAULT_INDENT))
