from xml.etree.ElementTree import Element

from fix2json.xml_logic.utils import (
    get_fuzzy,
    xml_get_docs,
    xml_get_history,
    xml_to_sorted_dict,
)


def xml_to_abbreviations(root: Element):
    return xml_to_sorted_dict(root, xml_to_abbreviation)


def xml_to_abbreviation(root: Element):
    return (
        # Primary key.
        get_fuzzy(root, "abbrTerm"),
        {
            "term": get_fuzzy(root, "term"),
            "docs": xml_get_docs(root),
            "history": xml_get_history(root),
        },
    )
