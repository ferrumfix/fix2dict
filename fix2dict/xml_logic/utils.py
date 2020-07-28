from natsort import natsorted

from ..fix_version import FixVersion


def get_fuzzy(elem, *keys):
    for key in list(keys):
        lower = key[0].lower() + key[1:]
        upper = key[0].upper() + key[1:]
        result = (
            elem.findtext(lower)
            or elem.findtext(upper)
            or elem.get(lower)
            or elem.get(upper)
        )
        if result is not None:
            return result


def filter_none(data):
    return {k: v for (k, v) in data.items() if v is not None}


def xml_get_docs(
    root, body=False, usage=False, volume=False, elaboration=False, examples=False,
):
    data = {}
    data["$id"] = root.get("textId")
    data["description"] = root.findtext("Description")
    data["usage"] = root.findtext("Usage")
    data["volume"] = root.findtext("Volume") or root.get("volume")
    data["elaboration"] = root.findtext("Elaboration")
    if examples:
        data["examples"] = [c.text for c in root.findall("Example")]
    return filter_none(data)


def xml_get_history(root, replaced=False):
    data = {}
    keywords = ["added", "updated", "deprecated"]
    if replaced:
        keywords.append("replaced")
        if root.get("ReplacedByField") is not None:
            data["replacement"] = root.get("ReplacedByField")
    for keyword in keywords:
        version = FixVersion.create_from_xml_attrs(root.attrib, keyword)
        if version is not None:
            data[keyword] = version.data
    if root.get("issue"):
        data["issues"] = [root.get("issue")]
    return filter_none(data)


def xml_to_sorted_dict(root, f):
    if root is None:
        root = []
    data = natsorted([f(c) for c in root])
    return {k: v for (k, v) in data}
