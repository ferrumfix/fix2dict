import unittest
from xml.etree import ElementTree

from fix2dict.fix_version import FixVersion


class TestFixVersionFromString(unittest.TestCase):
    def test_40(self):
        version = FixVersion("fix.4.0")
        self.assertEqual(
            version.data,
            {"fix": "fix", "major": "4", "minor": "0", "sp": "0"},
        )

    def test_50SP2EP254(self):
        version = FixVersion("fix.5.0SP2", ep="254")
        self.assertEqual(
            version.data,
            {"fix": "fix", "major": "5", "minor": "0", "sp": "2", "ep": "254"},
        )

    def test_fixt_11(self):
        version = FixVersion("fixt.1.1")
        self.assertEqual(
            version.data,
            {"fix": "fixt", "major": "1", "minor": "1", "sp": "0"},
        )


def xml_string_to_version(data, prefix):
    return FixVersion.create_from_xml_attrs(
        ElementTree.fromstring(data).attrib, prefix
    ).data


class TestFixVersionFromXML(unittest.TestCase):
    def test_updated_50SP1EP97(self):
        data = """
        <Message
            updated="FIX.5.0SP1"
            updatedEP="97"
            added="FIX.4.4"
            addedEP="-1">
        </Message>
        """
        self.assertEqual(
            xml_string_to_version(data, "updated"),
            {"fix": "fix", "major": "5", "minor": "0", "sp": "1", "ep": "97"},
        )

    def test_added_44(self):
        data = """
        <Component
            updated="FIX.5.0SP1"
            updatedEP="97"
            added="FIX.4.4"
            addedEP="-1">
        </Component>
        """
        self.assertEqual(
            xml_string_to_version(data, "added"),
            {"fix": "fix", "major": "4", "minor": "4", "sp": "0"},
        )
