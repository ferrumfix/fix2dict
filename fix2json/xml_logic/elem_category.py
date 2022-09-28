from xml.etree.ElementTree import Element

from fix2json.xml_logic.utils import (
    filter_none,
    get_fuzzy,
    xml_get_docs,
    xml_get_history,
    xml_to_sorted_dict,
)


def xml_to_categories(root: Element):
    return xml_to_sorted_dict(root, xml_to_category)


def xml_to_category(root: Element):
    return (
        # Primary key.
        get_fuzzy(root, "Id", "CategoryID", "Name"),
        {
            "kind": str.lower(get_fuzzy(root, "ComponentType")),
            "section": get_fuzzy(root, "Section", "SectionID"),
            "fixml": {
                "filename": get_fuzzy(root, "FIXMLFileName"),
                "generateImpl": get_fuzzy(root, "GenerateImplFile"),
                "optional": (lambda x: bool(int(x)) if x is not None else None)(
                    get_fuzzy(root, "NotReqXML")
                ),
            },
            "docs": xml_get_docs(root),
            "history": xml_get_history(root),
        },
    )
