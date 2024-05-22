import unittest
from ccptools.dtu.structs import *
from ccptools.dtu.casting import *


class TestInstant(unittest.TestCase):
    def test_instant_to_datetime(self):
        _dt = Datetime(2024, 5, 22, 10, 37, 54, 123000)
        self.assertEqual(_dt, instant_to_datetime(1716374274123))
