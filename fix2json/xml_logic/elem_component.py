from xml.etree.ElementTree import Element

from fix2json.xml_logic.utils import (
    filter_none,
    get_fuzzy,
    xml_get_docs,
    xml_get_history,
    xml_to_sorted_dict,
)


def xml_to_components(root: Element):
    return xml_to_sorted_dict(root, xml_to_component)


def xml_to_component(root: Element):
    kind = get_fuzzy(root, "type", "ComponentType")
    return (
        # Primary key.
        get_fuzzy(root, "id", "ComponentID"),
        filter_none(
            {
                "name": get_fuzzy(root, "name"),
                "nameAbbr": get_fuzzy(root, "abbrName", "nameAbbr"),
                "kind": kind.lower() if kind else None,
                "category": get_fuzzy(root, "category", "categoryID"),
                "docs": xml_get_docs(root, body=True, elaboration=True),
                "history": xml_get_history(root),
            }
        ),
    )


def embed_msg_contents_into_component(component, id, msg_contents):
    component["contents"] = msg_contents[id]
