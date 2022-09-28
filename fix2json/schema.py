import json

import jsonschema
import pkg_resources

fix2json_JSON_SCHEMA = pkg_resources.resource_string(
    "fix2json", "resources/fix2json-json-schema.json"
).decode("ascii")


def validate_fix2json_json(data):
    try:
        jsonschema.validate(data, json.loads(fix2json_JSON_SCHEMA))
    except jsonschema.ValidationError as e:
        print(e.message)
