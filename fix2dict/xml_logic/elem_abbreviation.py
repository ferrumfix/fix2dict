from .utils import xml_to_sorted_dict, xml_get_history, xml_get_docs, get_fuzzy


def xml_to_abbreviations(root):
    return xml_to_sorted_dict(root, xml_to_abbreviation)


def xml_to_abbreviation(root):
    return (
        # Primary key.
        get_fuzzy(root, "abbrTerm"),
        {
            "term": get_fuzzy(root, "term"),
            "docs": xml_get_docs(root),
            "history": xml_get_history(root),
        },
    )
