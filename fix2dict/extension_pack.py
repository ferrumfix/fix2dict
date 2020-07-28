from xml.etree.ElementTree import Element
import jsonpatch

from .xml_logic import (
    xml_to_abbreviation,
    xml_to_component,
    xml_to_datatype,
    xml_to_field,
    xml_to_category,
    xml_to_section,
)


class ExtensionPack:

    RESOURCE_RECIPES = [
        ["abbreviations", "Abbreviations", "Abbreviation", xml_to_abbreviation,],
        ["components", "Components", "Component", xml_to_component],
        ["datatypes", "Datatypes", "Datatype", xml_to_datatype],
        ["fields", "Fields", "Field", xml_to_field],
        ["categories", "Categories", "Category", xml_to_category],
        ["sections", "Sections", "Section", xml_to_section],
    ]

    def __init__(self, root: Element):
        self.id = root.get("id")
        self.approved = root.get("approved")
        self.description = root.get("desc")
        self.changes_added = {}
        self.changes_updated = {}
        self.changes_deprecated = {}
        self.changes_removed = {}
        self.populate_changes(root)

    def populate_changes(self, root: Element):
        for recipe in ExtensionPack.RESOURCE_RECIPES:
            kind = recipe[0]
            self.changes_added[kind] = {}
            self.changes_updated[kind] = {}
            self.changes_deprecated[kind] = {}
            self.changes_removed[kind] = {}
            for child in root.findall(recipe[1]):
                added = child.find("Inserts")
                updated = child.find("Updates")
                if added is not None:
                    for subchild in added.findall(recipe[2]):
                        self.changes_added[kind].update(dict([recipe[3](subchild)]))
                if updated is not None:
                    for child in updated.findall(recipe[2]):
                        self.changes_updated[kind].update(dict([recipe[3](child)]))

    def get_addition_as_jsonpatch(self, resource_kind, key):
        return [
            {
                "op": "add",
                "path": "/{}/{}".format(resource_kind, key),
                "value": self.changes_added[resource_kind][key],
            }
        ]

    def get_update_as_jsonpatch(self, resource_kind, key):
        data = []
        for (c_key, c_value) in self.changes_updated[resource_kind][key].items():
            data.append(
                {
                    "op": "replace",
                    "path": "/{}/{}/{}".format(resource_kind, key, c_key),
                    "value": c_value,
                }
            )
        return data

    def get_deprecation_as_jsonpatch(self, resource_kind, key):
        # TODO
        return []

    def get_removal_as_jsonpatch(self, resource_kind, key):
        return [{"op": "remove", "path": "/{}/{}".format(resource_kind, key)}]

    def to_jsonpatch(self):
        data = []
        # TODO: JSONPatch for metadata.
        for recipe in ExtensionPack.RESOURCE_RECIPES:
            kind = recipe[0]
            for key in self.changes_added[kind].keys():
                data += self.get_addition_as_jsonpatch(kind, key)
            for key in self.changes_updated[kind].keys():
                data += self.get_update_as_jsonpatch(kind, key)
            for key in self.changes_deprecated[kind].keys():
                data += self.get_deprecation_as_jsonpatch(kind, key)
            for key in self.changes_removed[kind].keys():
                data += self.get_removal_as_jsonpatch(kind, key)
        data.append({"op": "add", "path": "/meta/version/ep/-", "value": self.id})
        return jsonpatch.JsonPatch(data)
