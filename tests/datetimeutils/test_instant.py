import unittest
from ccptools.dtu.structs import *
from ccptools.dtu.casting import *


def _millisec_resolution(dt: Datetime) -> Datetime:
    return dt.replace(microsecond=int(dt.microsecond / 1000.)*1000)


class TestInstant(unittest.TestCase):
    def test_instant_to_datetime(self):
        _dt = Datetime(2024, 5, 22, 10, 37, 54, 123000)
        self.assertEqual(_dt, _millisec_resolution(instant_to_datetime(1716374274123)))

        _dt = Datetime(1024, 5, 22, 10, 37, 54, 987000)
        self.assertEqual(_dt, _millisec_resolution(instant_to_datetime(-29840620925013)))

        _dt = Datetime(3024, 5, 22, 10, 37, 54, 123000)
        self.assertEqual(_dt, _millisec_resolution(instant_to_datetime(33273283074123)))
