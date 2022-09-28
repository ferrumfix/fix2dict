from jsonpatch import JsonPatch, JsonPatchException

from fix2json.schema import validate_fix2json_json


def apply_patch(data, patch: JsonPatch):
    validate_fix2json_json(data)
    try:
        data = patch.apply(data)
    except Exception as e:
        print(e)
    # TODO: meta and history stuff.
    return data
