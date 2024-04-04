import unittest

from ccptools import dtu


class FiletimeTest(unittest.TestCase):
    def test_filetime_to_datetime(self):
        def assertSame(filetime, date_tuple):
            self.assertEqual(dtu.filetime_to_datetime(filetime), dtu.Datetime(*date_tuple))

        assertSame(0, (1601, 1, 1, 0, 0, 0, 0))
        assertSame(10, (1601, 1, 1, 0, 0, 0, 1))
        assertSame(10000000, (1601, 1, 1, 0, 0, 1, 0))
        assertSame(119445914047564820, (1979, 7, 6, 14, 3, 24, 756482))
        # assertSame(2650467743999999990, (9999, 12, 31, 23, 59, 59, 999999))  # OUT OF date RANGE :(
        assertSame(-504911232000000000, (1, 1, 1, 0, 0, 0, 0))
        assertSame(130096156280000100, (2013, 4, 5, 6, 7, 8, 10))

        self.assertRaises(OverflowError, dtu.filetime_to_datetime, 2650467744000000000)

    def test_datetime_to_filetime(self):
        def assertSame(date_tuple, filetime):
            self.assertEqual(dtu.datetime_to_filetime(dtu.Datetime(*date_tuple)), filetime)

        assertSame((1601, 1, 1, 0, 0, 0, 0), 0)
        assertSame((1601, 1, 1, 0, 0, 0, 1), 10)
        assertSame((1601, 1, 1, 0, 0, 1, 0), 10000000)
        assertSame((1979, 7, 6, 14, 3, 24, 756482), 119445914047564820)
        assertSame((9999, 12, 31, 23, 59, 59, 999999), 2650467743999999990)
        assertSame((1, 1, 1, 0, 0, 0, 0), -504911232000000000)
        assertSame((2013, 4, 5, 6, 7, 8, 10), 130096156280000100)
