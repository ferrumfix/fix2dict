from xml.etree.ElementTree import Element

from fix2json.xml_logic.utils import (
    filter_none,
    get_fuzzy,
    xml_get_docs,
    xml_get_history,
    xml_to_sorted_dict,
)


def xml_to_datatypes(root: Element):
    if root is None:
        root = []
    data = [xml_to_datatype(c) for c in root]
    return {k: v for (k, v) in data}


def xml_to_datatype(root: Element):
    return (
        # Primary key.
        get_fuzzy(root, "name"),
        filter_none(
            {
                "base": get_fuzzy(root, "baseType", "base"),
                "docs": xml_get_docs(root, examples=True, body=True),
                "history": xml_get_history(root),
            }
        ),
    )
