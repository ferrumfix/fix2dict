import unittest

from fix2json.resources import test_cases
from fix2json.xml_logic import xml_to_field


class TestElemField(unittest.TestCase):
    def test_expected(self):
        for (original, expected) in test_cases("fields"):
            self.assertEqual(xml_to_field(original), tuple(expected))
