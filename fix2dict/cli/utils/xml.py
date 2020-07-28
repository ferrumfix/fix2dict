import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from . import err


def strip_namespace(el: Element):
    if el.tag.startswith("{"):
        el.tag = el.tag.split("}", 1)[1]  # strip namespace
    key_replacements = {}
    for k in el.attrib.keys():
        if k.startswith("{"):
            k2 = k.split("}", 1)[1]
            key_replacements[k2] = k
    for (new_k, old_k) in key_replacements.items():
        el.attrib[new_k] = el.attrib[old_k]
        del el.attrib[old_k]
    for child in el:
        strip_namespace(child)


def read_xml_root(src, filename, opt=True):
    path = os.path.join(src, filename)
    try:
        root = ElementTree.parse(path).getroot()
        strip_namespace(root)
        return root
    except (ElementTree.ParseError, FileNotFoundError):
        if not opt:
            err("XML")
    return None
