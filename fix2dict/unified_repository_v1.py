from .__version__ import __version__
from .resources import LEGAL_INFO
from .fix_version import FixVersion
import sys
from xml.etree.ElementTree import Element

from .fix_version import FixVersion
from .utils import iso8601_utc
from .xml_logic import (
    xml_to_abbreviations,
    xml_to_categories,
    xml_to_components,
    xml_to_datatypes,
    xml_to_docs_definitions,
    xml_to_enums,
    xml_to_fields,
    xml_to_messages,
    xml_to_msg_contents,
    xml_to_sections,
    embed_enums_into_field,
    embed_msg_contents_into_message,
    embed_msg_contents_into_component,
    embed_docs,
)


def transform_unified_repository_v1(root: Element, phrases: Element):
    abbreviations = xml_to_abbreviations(root.find("abbreviations"))
    categories = xml_to_categories(root.find("categories"))
    components = xml_to_components(root.find("components"))
    datatypes = xml_to_datatypes(root.find("datatypes"))
    fields = xml_to_fields(root.find("fields"))
    messages = xml_to_messages(root.find("messages"))
    sections = xml_to_sections(root.find("sections"))
    fix_version = FixVersion.create_from_xml_attrs(root.attrib, "version").data
    phrases = xml_to_docs_definitions(phrases)
    # Embed docstrings into elements.
    embed_docs(abbreviations, phrases)
    embed_docs(categories, phrases)
    embed_docs(components, phrases)
    embed_docs(datatypes, phrases)
    embed_docs(fields, phrases)
    embed_docs(messages, phrases)
    embed_docs(sections, phrases)
    # No other embeddings to worry about. The Unified FIX Repository contains
    # hierarchial data already.
    return {
        "meta": {
            "schema": "1",
            "version": fix_version,
            "copyright": "Copyright (c) FIX Protocol Limited, all rights reserved",
            "fix2dict": {
                "version": __version__,
                "legal": LEGAL_INFO,
                "md5": "",
                "command": " ".join(sys.argv),
                "timestamp": iso8601_utc(),
            },
        },
        "abbreviations": abbreviations,
        "datatypes": datatypes,
        "sections": sections,
        "categories": categories,
        "fields": fields,
        "components": components,
        "messages": messages,
    }
