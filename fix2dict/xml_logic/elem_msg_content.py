from .utils import (
    xml_to_sorted_dict,
    xml_get_docs,
    xml_get_history,
    filter_none,
    get_fuzzy,
)


def xml_to_msg_contents(root):
    data = {}
    for child in root:
        elem = xml_to_msg_content(child)
        parent = elem["$parent"]
        if parent not in data:
            data[parent] = []
        data[parent].append(elem)
    return {k: sorted(v, key=lambda x: x["position"]) for (k, v) in data.items()}


def xml_to_msg_content(root):
    return {
        "$parent": get_fuzzy(root, "ComponentID"),
        "tag": get_fuzzy(root, "TagText"),
        "kind": None,
        "position": float(get_fuzzy(root, "Position")),
        "optional": not bool(int(get_fuzzy(root, "Reqd"))),
        "inlined": bool(int(get_fuzzy(root, "Inlined") or "1")),
        "docs": xml_get_docs(root, body=True),
        "history": xml_get_history(root),
    }
