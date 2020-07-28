import click
import jsonpatch
import json
import os
from checksumdir import dirhash

from . import cli
from .utils.options import opt_patch
from .utils.xml import read_xml_root
from .utils.json import read_json, DEFAULT_INDENT
from ..unified_repository_v1 import transform_unified_repository_v1
from ..fix_version import FixVersion
from ..schema import validate_v1
from ..patch import apply_patch


@cli.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
@click.argument("phrases", nargs=1, type=click.Path(exists=True))
def repo_u(src, phrases):
    """
    Transform a Unified FIX Repository data into JSON.

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
    root = read_xml_root("", src, opt=False)[8]
    phrases = read_xml_root("", phrases, opt=False)
    data = transform_unified_repository_v1(root, phrases)
    print(json.dumps(data, indent=DEFAULT_INDENT))
