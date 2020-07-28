from .utils import (
    xml_to_sorted_dict,
    xml_get_history,
    xml_get_docs,
    filter_none,
    get_fuzzy,
)


def xml_to_components(root):
    return xml_to_sorted_dict(root, xml_to_component)


def xml_to_component(root):
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
