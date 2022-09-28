import datetime
import unittest

from fix2json.utils import iso8601_utc


class TestTimestamp(unittest.TestCase):
    def test_is_valid_iso8601(self):
        datetime.datetime.strptime(iso8601_utc(), "%Y-%m-%dT%H:%M:%SZ")
