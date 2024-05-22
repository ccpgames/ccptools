import unittest
from ccptools.dtu.structs import *
from ccptools.dtu.casting import *


def _10_microsec_resolution(dt: Datetime) -> Datetime:
    return dt.replace(microsecond=int(dt.microsecond / 10.)*10)


class TestInstant(unittest.TestCase):
    def test_instant_to_datetime(self):
        _dt = Datetime(2024, 5, 22, 10, 37, 54, 123456)
        self.assertEqual(_10_microsec_resolution(_dt), _10_microsec_resolution(timestamp_to_datetime(1716374274.123456)))

        _dt = Datetime(1024, 5, 22, 10, 37, 54, 987654)
        self.assertEqual(_10_microsec_resolution(_dt), _10_microsec_resolution(timestamp_to_datetime(-29840620925.012344)))

        _dt = Datetime(3024, 5, 22, 10, 37, 54, 123456)
        self.assertEqual(_10_microsec_resolution(_dt), _10_microsec_resolution(timestamp_to_datetime(33273283074.123456)))
