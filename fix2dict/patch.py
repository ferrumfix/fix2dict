from jsonpatch import JsonPatch, JsonPatchException

from .schema import validate_v1


def apply_patch(data, patch: JsonPatch):
    validate_v1(data)
    try:
        data = patch.apply(data)
    except Exception as e:
        print(e)
    # TODO: meta and history stuff.
    return data
