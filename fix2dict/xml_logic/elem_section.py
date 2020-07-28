from .utils import (
    xml_to_sorted_dict,
    xml_get_docs,
    xml_get_history,
    filter_none,
    get_fuzzy,
)


def xml_to_sections(root):
    if root is None:
        root = []
    data = [xml_to_section(c) for c in root]
    return {k: v for (k, v) in data}


def xml_to_section(root):
    return (
        # Primary key.
        get_fuzzy(root, "Id", "SectionID", "Name"),
        {
            "name": get_fuzzy(root, "Name"),
            "fixml": {
                "filename": get_fuzzy(root, "FIXMLFileName"),
                "optional": (lambda x: bool(int(x)) if x is not None else None)(
                    get_fuzzy(root, "NotReqXML")
                ),
            },
            "docs": xml_get_docs(root, volume=True, body=True),
            "history": xml_get_history(root),
        },
    )
