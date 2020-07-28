from .utils import (
    xml_to_sorted_dict,
    xml_get_docs,
    xml_get_history,
    filter_none,
    get_fuzzy,
)


def xml_to_datatypes(root):
    if root is None:
        root = []
    data = [xml_to_datatype(c) for c in root]
    return {k: v for (k, v) in data}


def xml_to_datatype(root):
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
