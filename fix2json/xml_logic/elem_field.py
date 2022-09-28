from xml.etree.ElementTree import Element

from fix2json.xml_logic.utils import (
    filter_none,
    get_fuzzy,
    xml_get_docs,
    xml_get_history,
    xml_to_sorted_dict,
)

from .elem_enum import xml_to_enum


def xml_to_fields(root: Element):
    return xml_to_sorted_dict(root, xml_to_field)


def xml_to_field(root: Element):
    return (
        # Primary key.
        get_fuzzy(root, "id", "tag"),
        filter_none(
            {
                "name": get_fuzzy(root, "name"),
                "datatype": get_fuzzy(root, "type"),
                "enum": xml_get_enum(root),
                "docs": xml_get_docs(root, body=True, elaboration=True),
                "history": xml_get_history(root),
            }
        ),
    )


def xml_get_enum(root: Element):
    if len(root.findall("enum")) == 0:
        return get_fuzzy(root, "EnumDatatype")
    return [xml_to_enum(child) for child in root]


def embed_enums_into_field(field, enums):
    if "enum" in field:
        field["enum"] = enums[field["enum"]]
