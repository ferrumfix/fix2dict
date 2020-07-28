from .utils import xml_to_sorted_dict, xml_get_history, filter_none


def xml_to_docs_definitions(root):
    return xml_to_sorted_dict(root, xml_to_doc_definition)


def xml_to_doc_definition(root):
    text_id = root.get("textId", default="")
    kind = text_id[:2]
    docs = {
        "description": "",
        "elaboration": "",
    }
    # Abbreviation.
    if kind != "AT":
        docs["examples"] = []
    for child in root:
        if ("purpose", "SYNOPSIS") in child.attrib.items():
            for paragraph in child:
                docs["description"] += paragraph.text + "\n"
        if ("purpose", "ELABORATION") in child.attrib.items():
            for paragraph in child:
                docs["elaboration"] += paragraph.text + "\n"
    if docs["description"] == "":
        del docs["description"]
    if docs["elaboration"] == "":
        del docs["elaboration"]
    if kind == "AT":
        docs["$abbreviationTerm"] = root.find("text").findtext("para")
    return (text_id, docs)


def embed_docs(data, phrases):
    for val in data.values():
        if "$id" in val["docs"].keys():
            if val["docs"]["$id"].startswith("AT_"):
                val["term"] = phrases[val["docs"]["$id"]]["$abbreviationTerm"]
                del phrases[val["docs"]["$id"]]["$abbreviationTerm"]
            val["docs"] = phrases[val["docs"]["$id"]]
