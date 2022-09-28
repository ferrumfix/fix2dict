import unittest

from fix2json.resources import test_cases
from fix2json.xml_logic import xml_to_datatype


class TestElemDatatype(unittest.TestCase):
    def test_expected(self):
        for (original, expected) in test_cases("datatypes"):
            self.assertEqual(
                xml_to_datatype(original), tuple(expected))
