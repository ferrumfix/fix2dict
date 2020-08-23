import click
import jsonpatch
import json
import os
import sqlite3
from checksumdir import dirhash
from sqlite3 import Error

from . import cli
from .utils.options import opt_patch
from .utils.xml import read_xml_root
from ..formats.sqlite import dict_to_mem_sqlite
from ..formats.basic_repository_v1 import transform_basic_repository_v1
from ..formats.orchestra_v1 import transform_orchestra_v1
from .utils.json import read_json, DEFAULT_INDENT
from ..fix_version import FixVersion
from ..schema import validate_v1
from ..patch import apply_patch
from .utils.xml import read_xml_root
from .utils.json import beautify_json
from ..extension_pack import ExtensionPack
from ..formats.unified_repository_v1 import transform_unified_repository_v1

@cli.command()
@click.argument("fmt", nargs=1)
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def convert_repo(fmt, files):
    """
    Convert FIX Repository data from one format to another.
    """
    src = files[0]
    if fmt == "basic":
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
        data["meta"]["fix2dict"]["md5"] = dirhash(src, "md5")
        validate_v1(data)
        print(json.dumps(data, indent=DEFAULT_INDENT))
    elif fmt == "unified":
        root = read_xml_root("", src, opt=False)[8]
        phrases = read_xml_root("", phrases, opt=False)
        data = transform_unified_repository_v1(root, phrases)
        print(json.dumps(data, indent=DEFAULT_INDENT))
    elif fmt == "orchestra":
        root = read_xml_root("", src, opt=False)
        data = transform_orchestra_v1(root)
        print(json.dumps(data, indent=DEFAULT_INDENT))
    end = "sqlite3"
    if end == "sqlite3":
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