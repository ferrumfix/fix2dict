import unittest
from fix2dict.xml_logic import (
    xml_to_abbreviation,
)
from fix2dict.resources import test_cases


class TestElemAbbreviation(unittest.TestCase):
    def test_expected(self):
        for (original, expected) in test_cases("abbreviations"):
            self.assertEqual(xml_to_abbreviation(original), tuple(expected))
