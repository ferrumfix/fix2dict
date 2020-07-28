import pkg_resources
import json
import os
from xml.etree import ElementTree

PKG_NAME = "fix2dict"

LEGAL_INFO = (
    'FIX2dict is distributed on an "AS IS" BASIS, '
    "WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, "
    "either express or implied."
)


def test_cases(tag):
    data = []
    t_cases = pkg_resources.resource_listdir(
        PKG_NAME, "resources/tests/{}/".format(tag)
    )
    for t_case in t_cases:
        base, extension = os.path.splitext(t_case)
        if extension == ".xml":
            xml_string = pkg_resources.resource_string(
                PKG_NAME, "resources/tests/{}/{}.xml".format(tag, base)
            )
            json_string = pkg_resources.resource_string(
                PKG_NAME, "resources/tests/{}/{}.json".format(tag, base)
            )
            data.append((ElementTree.fromstring(xml_string), json.loads(json_string)))
    return data
