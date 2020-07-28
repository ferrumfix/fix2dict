import pkg_resources
import json
import jsonschema

JSON_SCHEMA_V1 = pkg_resources.resource_string(
    "fix2dict", "resources/schema/v1.json"
).decode("ascii")


def validate_v1(data):
    try:
        jsonschema.validate(data, json.loads(JSON_SCHEMA_V1))
    except jsonschema.ValidationError as e:
        print(e.message)
