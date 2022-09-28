import unittest

from fix2json.resources import test_cases
from fix2json.xml_logic import xml_to_abbreviation


class TestElemAbbreviation(unittest.TestCase):
    def test_expected(self):
        for (original, expected) in test_cases("abbreviations"):
            self.assertEqual(xml_to_abbreviation(original), tuple(expected))
