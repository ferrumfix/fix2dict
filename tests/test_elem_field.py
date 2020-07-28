import unittest
from fix2dict.xml_logic import (
    xml_to_field,
)
from fix2dict.resources import test_cases


class TestElemField(unittest.TestCase):
    def test_expected(self):
        for (original, expected) in test_cases("fields"):
            self.assertEqual(xml_to_field(original), tuple(expected))
