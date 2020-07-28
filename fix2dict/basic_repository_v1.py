from .__version__ import __version__
from .resources import LEGAL_INFO
from .fix_version import FixVersion
import sys
from xml.etree.ElementTree import Element

from .utils import iso8601_utc
from .xml_logic import (
    xml_to_abbreviations,
    xml_to_categories,
    xml_to_components,
    xml_to_datatypes,
    xml_to_enums,
    xml_to_fields,
    xml_to_messages,
    xml_to_msg_contents,
    xml_to_sections,
    embed_enums_into_field,
    embed_msg_contents_into_message,
    embed_msg_contents_into_component,
)
from .xml_logic.utils import get_fuzzy


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
    fix_version = FixVersion(get_fuzzy(messages, "version")).data
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
