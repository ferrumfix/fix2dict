import sys
from xml.etree.ElementTree import Element

from ..fix_version import FixVersion
from ..__version__ import __version__
from ..utils import iso8601_utc
from ..resources import LEGAL_INFO
from ..xml_logic import (
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
from ..xml_logic.utils import get_fuzzy



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