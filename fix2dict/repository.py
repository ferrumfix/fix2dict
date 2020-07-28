import sys
from xml.etree.ElementTree import Element

from .fix_version import FixVersion
from .__version__ import __version__
from .utils import iso8601_utc
from .resources import LEGAL_INFO
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
from .xml_logic.utils import get_fuzzy


def meta_v1(fix_version):
    return {
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
    }


def transform_basic_repository_v1(
    abbreviations: Element,
    categories: Element,
    components: Element,
    datatypes: Element,
    enums: Element,
    fields: Element,
    messages: Element,
    msg_contents: Element,
    sections: Element,
):
    fix_version = FixVersion.create_from_xml_attrs(
        messages.attrib, "version").data
    abbreviations = xml_to_abbreviations(abbreviations)
    categories = xml_to_categories(categories)
    components = xml_to_components(components)
    datatypes = xml_to_datatypes(datatypes)
    enums = xml_to_enums(enums)
    fields = xml_to_fields(fields)
    messages = xml_to_messages(messages)
    msg_contents = xml_to_msg_contents(msg_contents)
    sections = xml_to_sections(sections)
    # Embeddings.
    for val in fields.values():
        embed_enums_into_field(val, enums)
    for val in messages.values():
        embed_msg_contents_into_message(val, msg_contents)
    for (key, val) in components.items():
        embed_msg_contents_into_component(val, key, msg_contents)
    # Check the kind of content inside messages.
    for (message_id, msg_contents_by_tag) in msg_contents.items():
        for element in msg_contents_by_tag:
            if element["tag"] in fields:
                element["kind"] = "field"
            elif element["tag"] in [c["name"] for c in components.values()]:
                element["kind"] = "component"
            else:
                print(
                    "-- UNKNOWN MSG_CONTENTS with msg. id {} and tag {}".format(
                        message_id, element["tag"]
                    ),
                    file=sys.stderr,
                )
    return {
        "meta": meta_v1(fix_version),
        "abbreviations": abbreviations,
        "datatypes": datatypes,
        "sections": sections,
        "categories": categories,
        "fields": fields,
        "components": components,
        "messages": messages,
    }


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
        "meta": meta_v1(fix_version),
        "abbreviations": abbreviations,
        "datatypes": datatypes,
        "sections": sections,
        "categories": categories,
        "fields": fields,
        "components": components,
        "messages": messages,
    }


def transform_orchestra_v1(root: Element):
    abbreviations = xml_to_abbreviations(root.find("abbreviations"))
    categories = xml_to_categories(root.find("categories"))
    components = xml_to_components(root.find("components"))
    datatypes = xml_to_datatypes(root.find("datatypes"))
    enums = xml_to_enums(root.finds("codesets"))  # FIXME
    fields = xml_to_fields(root.find("fields"))
    messages = xml_to_messages(root.find("messages"))
    sections = xml_to_sections(root.find("sections"))
    fix_version = FixVersion.create_from_xml_attrs(root.attrib, "version").data
    return {
        "meta": meta_v1(fix_version),
        "abbreviations": abbreviations,
        "datatypes": datatypes,
        "sections": sections,
        "categories": categories,
        "fields": fields,
        "components": components,
        "messages": messages,
    }
