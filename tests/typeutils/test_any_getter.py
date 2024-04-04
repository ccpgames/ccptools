import unittest

from ccptools.legacyapi.typeutils import iters
import datetime


class TestAnyGetter(unittest.TestCase):
    def test_any_getter(self):
        lennon = datetime.date(1940, 10, 9)

        self.assertEqual(1940, iters.any_getter(lennon, 'year'))
        self.assertEqual('n', iters.any_getter('lennon', -1))
        self.assertEqual(2, iters.any_getter(lennon, 'weekday', eval_call=True))
