import unittest
import datetime

from ccptools.legacyapi import datetimeutils


class DateTimeUtilsTest(unittest.TestCase):
    def test_filetime_to_datetime(self):
        def assertSame(filetime, date_tuple):
            self.assertEqual(datetimeutils.filetime_to_datetime(filetime), datetime.datetime(*date_tuple))

        assertSame(0, (1601, 1, 1, 0, 0, 0, 0))
        assertSame(10, (1601, 1, 1, 0, 0, 0, 1))
        assertSame(10000000, (1601, 1, 1, 0, 0, 1, 0))
        assertSame(119445914047564820, (1979, 7, 6, 14, 3, 24, 756482))
        # assertSame(2650467743999999990, (9999, 12, 31, 23, 59, 59, 999999))  # OUT OF date RANGE :(
        assertSame(-504911232000000000, (1, 1, 1, 0, 0, 0, 0))
        assertSame(130096156280000100, (2013, 4, 5, 6, 7, 8, 10))

        self.assertRaises(OverflowError, datetimeutils.filetime_to_datetime, 2650467744000000000)

    def test_datetime_to_filetime(self):
        def assertSame(date_tuple, filetime):
            self.assertEqual(datetimeutils.datetime_to_filetime(datetime.datetime(*date_tuple)), filetime)

        assertSame((1601, 1, 1, 0, 0, 0, 0), 0)
        assertSame((1601, 1, 1, 0, 0, 0, 1), 10)
        assertSame((1601, 1, 1, 0, 0, 1, 0), 10000000)
        assertSame((1979, 7, 6, 14, 3, 24, 756482), 119445914047564820)
        assertSame((9999, 12, 31, 23, 59, 59, 999999), 2650467743999999990)
        assertSame((1, 1, 1, 0, 0, 0, 0), -504911232000000000)
        assertSame((2013, 4, 5, 6, 7, 8, 10), 130096156280000100)

    def test_any_to_datetime(self):
        def assertSame(value, expected):
            if isinstance(expected, tuple):
                expected = datetime.datetime(*expected)
            self.assertEqual(datetimeutils.any_to_datetime(value), expected)

        def assertDefault(value):
            self.assertEqual(datetimeutils.any_to_datetime(value, 42), 42)

        assertSame(datetime.datetime(1979, 7, 6, 14, 3, 24, 756482), (1979, 7, 6, 14, 3, 24, 756482))
        assertSame(datetime.date(1979, 7, 6), (1979, 7, 6, 0, 0, 0, 0))
        assertSame(119445914047564820, (1979, 7, 6, 14, 3, 24, 756482))
        assertSame(300117804, (1979, 7, 6, 14, 3, 24))
        assertSame(300117804.321321, (1979, 7, 6, 14, 3, 24, 321321))
        assertSame(1570875489.134, (2019, 10, 12, 10, 18, 9, 134000))
        assertSame(100000000000, (1601, 1, 1, 2, 46, 40))

        assertSame(None, None)
        assertSame('2013-06-10T12:13:14', (2013, 6, 10, 12, 13, 14))
        now = datetime.datetime.now()
        assertSame('12:13:14', (now.year, now.month, now.day, 12, 13, 14))
        assertSame('1 2 3 4 5 6 7', (1, 2, 3, 4, 5, 6, 7))
        assertSame('9999\\12/31@23,59.59,999999', (9999, 12, 31, 23, 59, 59, 999999))
        assertSame('9999\\12/31@23,59.59,999999999', (9999, 12, 31, 23, 59, 59, 999999))
        assertSame('9999\\12/31@23,59.59,999999999', (9999, 12, 31, 23, 59, 59, 999999))
        assertSame(29999999999, (2920, 8, 30, 5, 19, 59))
        assertSame(2650467744000000000, 2650467744000000000)

        assertDefault(None)
        assertDefault('2013-99-10T12:13:14')
        assertDefault(2650467744000000000)

    def test_isostr_to_datetime_seq(self):
        def assertSame(value, expected):
            if isinstance(expected, tuple):
                expected = datetime.datetime(*expected)
            self.assertEqual(datetimeutils.any_to_datetime(value), expected)

        def assertFails(value):
            self.assertEqual(datetimeutils.any_to_datetime(value, None), None)

        for y in range(1, 10):
            assertSame('0%s-01-01T00:00:00' % y, (y, 1, 1, 0, 0, 0))
            assertSame('00%s-01-01T00:00:00' % y, (y, 1, 1, 0, 0, 0))
            assertSame('000%s-01-01T00:00:00' % y, (y, 1, 1, 0, 0, 0))
            assertSame('00%s0-01-01T00:00:00' % y, (y*10, 1, 1, 0, 0, 0))
            assertSame('0%s00-01-01T00:00:00' % y, (y*100, 1, 1, 0, 0, 0))

        for y in range(1, 10000):
            assertSame('%s-01-01T00:00:00' % y, (y, 1, 1, 0, 0, 0))
        assertFails('0-01-01T00:00:00')
        assertFails('10000-01-01T00:00:00')

        for m in range(1, 10):
            assertSame('2013-0%s-01T00:00:00' % m, (2013, m, 1, 0, 0, 0))
        for m in range(1, 13):
            assertSame('2013-%s-01T00:00:00' % m, (2013, m, 1, 0, 0, 0))
        assertFails('2013-0-01T00:00:00')
        assertFails('2013-13-01T00:00:00')

        for d in range(1, 10):
            assertSame('2013-01-0%sT00:00:00' % d, (2013, 1, d, 0, 0, 0))
        for d in range(1, 32):
            assertSame('2013-01-%sT00:00:00' % d, (2013, 1, d, 0, 0, 0))
        assertFails('2013-01-0T00:00:00')
        assertSame('2013-01-32T00:00:00', (2013, 1, 3, 0, 0, 0))

        now = datetime.datetime.now()

        for h in range(10):
            assertSame('2013-01-01T0%s:00:00' % h, (2013, 1, 1, h, 0, 0))
        for h in range(24):
            assertSame('2013-01-01T%s:00:00' % h, (2013, 1, 1, h, 0, 0))
            assertSame('2013-01-01T%02d:00:00' % h, (2013, 1, 1, h, 0, 0))
            assertSame('2013-01-01T%s:00' % h, (2013, 1, 1, h, 0, 0))
            assertSame('2013-01-01T%02d:00' % h, (2013, 1, 1, h, 0, 0))
            assertSame('%02d:00:00' % h, (now.year, now.month, now.day, h, 0, 0))
            assertSame('%s:00:00' % h, (now.year, now.month, now.day, h, 0, 0))
            assertSame('%02d:00' % h, (now.year, now.month, now.day, h, 0, 0))
            assertSame('%s:00' % h, (now.year, now.month, now.day, h, 0, 0))
            assertSame('%02d:0' % h, (now.year, now.month, now.day, h, 0, 0))
            assertSame('%s:0' % h, (now.year, now.month, now.day, h, 0, 0))
        assertSame('2013-01-01T-1:00:00', (2013, 1, 1, 0, 0, 0))
        assertSame('2013-01-01T:00:00', (2013, 1, 1, 0, 0, 0))
        assertSame('2013-01-01T24:00:00', (2013, 1, 1, 0, 0, 0))

        for ms in range(10):
            assertSame('2013-01-01T00:0%s:00' % ms, (2013, 1, 1, 0, ms, 0))
            assertSame('2013-01-01T00:00:0%s' % ms, (2013, 1, 1, 0, 0, ms))
        for ms in range(24):
            assertSame('2013-01-01T00:%s:00' % ms, (2013, 1, 1, 0, ms, 0))
            assertSame('2013-01-01T00:00:%s' % ms, (2013, 1, 1, 0, 0, ms))

        assertSame('2013-01-01T00::00', (2013, 1, 1, 0, 0, 0))
        assertSame('2013-01-01T00:-1:00', (2013, 1, 1, 0, 0, 0))
        assertSame('2013-01-01T00:60:00', (2013, 1, 1, 0, 6, 0))
        assertSame('2013-01-01T00:00:', (2013, 1, 1, 0, 0, 0))
        assertSame('2013-01-01T00:00:-1', (2013, 1, 1, 0, 0, 0))
        assertSame('2013-01-01T00:00:60', (2013, 1, 1, 0, 0, 6))

    def test_ago(self):
        def assertOutput(delta, expected):
            self.assertEqual(datetimeutils.ago(delta), expected)

        assertOutput(datetime.timedelta(days=2002, seconds=20000), '5 years')
        assertOutput(datetime.timedelta(days=366, seconds=20000), '1 year and 5 hours')
        assertOutput(datetime.timedelta(seconds=360), '6 minutes')
        assertOutput(datetime.timedelta(seconds=90), '1 minute')
        assertOutput(datetime.timedelta(seconds=59), 'a few seconds')

    def test_find_earliest_time_after_datetime(self):
        def _assert_earliest_time_equals(start, seek_time, expected):
            datetime_start = datetime.datetime(*start)
            time = datetime.time(*seek_time)
            datetime_expected = datetime.datetime(*expected)
            self.assertEqual(datetimeutils.find_earliest_time_after_datetime(datetime_start, time), datetime_expected)

        _assert_earliest_time_equals((2015, 5, 29, 12, 0), (9, 0), (2015, 5, 30, 9, 0))
        _assert_earliest_time_equals((2015, 5, 29, 12, 0), (12, 0), (2015, 5, 30, 12, 0))
        _assert_earliest_time_equals((2015, 5, 29, 12, 0), (15, 0), (2015, 5, 29, 15, 0))

        _assert_earliest_time_equals((2015, 5, 29, 12, 30), (9, 0), (2015, 5, 30, 9, 0))
        _assert_earliest_time_equals((2015, 5, 29, 12, 30), (12, 0), (2015, 5, 30, 12, 0))
        _assert_earliest_time_equals((2015, 5, 29, 12, 30), (13, 0), (2015, 5, 29, 13, 0))
        _assert_earliest_time_equals((2015, 5, 29, 12, 30), (15, 0), (2015, 5, 29, 15, 0))

        _assert_earliest_time_equals((2015, 5, 29, 12, 0), (9, 30), (2015, 5, 30, 9, 30))
        _assert_earliest_time_equals((2015, 5, 29, 12, 0), (11, 30), (2015, 5, 30, 11, 30))
        _assert_earliest_time_equals((2015, 5, 29, 12, 0), (12, 30), (2015, 5, 29, 12, 30))
        _assert_earliest_time_equals((2015, 5, 29, 12, 0), (15, 30), (2015, 5, 29, 15, 30))

    def test_str_to_timedelta(self):
        self.assertEqual(datetimeutils.str_to_timedelta('1d'), datetime.timedelta(days=1))
        self.assertEqual(datetimeutils.str_to_timedelta('2d'), datetime.timedelta(days=2))
        self.assertEqual(datetimeutils.str_to_timedelta('2days'), datetime.timedelta(days=2))
        self.assertEqual(datetimeutils.str_to_timedelta('+3days'), datetime.timedelta(days=3))
        self.assertEqual(datetimeutils.str_to_timedelta('-4days'), datetime.timedelta(days=-4))
        self.assertEqual(datetimeutils.str_to_timedelta('5d 1h'), datetime.timedelta(days=5, hours=1))
        self.assertEqual(datetimeutils.str_to_timedelta('6d 1.5h'), datetime.timedelta(days=6, hours=1.5))
        self.assertEqual(datetimeutils.str_to_timedelta('+6.5d11h59m'), datetime.timedelta(days=6.5, hours=11, minutes=59))
        self.assertEqual(datetimeutils.str_to_timedelta('7d-1m'), datetime.timedelta(days=6.5, hours=11, minutes=59))
        self.assertNotEqual(datetimeutils.str_to_timedelta('7d'), datetime.timedelta(days=6.5, hours=11, minutes=59))
        self.assertEqual(datetimeutils.str_to_timedelta('7foobars'), datetime.timedelta(seconds=0))
        self.assertEqual(datetimeutils.str_to_timedelta('7foobars', 7), 7)
        self.assertIsNone(datetimeutils.str_to_timedelta('7foobars', None))
    
    def test_find_earliest_time_and_weekday_after_datetime(self):
        def _assert_earliest_time_equals(start, seek_time_of_day, seek_day_of_week, expected):
            datetime_start = datetime.datetime(*start)
            time_of_day = datetime.time(*seek_time_of_day)
            datetime_expected = datetime.datetime(*expected)

            datetime_result = datetimeutils.find_earliest_time_and_weekday_after_datetime(datetime_start, time_of_day, seek_day_of_week)

            self.assertEqual(datetime_result, datetime_expected)
            self.assertEqual(datetime_result.weekday(), seek_day_of_week)

        # 2017-11-16 is a Thursday (weekday=3)
        _assert_earliest_time_equals((2017, 11, 16, 12, 0), (9, 0), 3, (2017, 11, 23, 9, 0))
        _assert_earliest_time_equals((2017, 11, 16, 12, 0), (12, 0), 3, (2017, 11, 23, 12, 0))
        _assert_earliest_time_equals((2017, 11, 16, 12, 0), (15, 0), 3, (2017, 11, 16, 15, 0))

        _assert_earliest_time_equals((2017, 11, 16, 12, 30), (9, 0), 3, (2017, 11, 23, 9, 0))
        _assert_earliest_time_equals((2017, 11, 16, 12, 30), (12, 0), 3, (2017, 11, 23, 12, 0))
        _assert_earliest_time_equals((2017, 11, 16, 12, 30), (13, 0), 3, (2017, 11, 16, 13, 0))
        _assert_earliest_time_equals((2017, 11, 16, 12, 30), (15, 0), 3, (2017, 11, 16, 15, 0))

        _assert_earliest_time_equals((2017, 11, 16, 12, 0), (9, 30), 3, (2017, 11, 23, 9, 30))
        _assert_earliest_time_equals((2017, 11, 16, 12, 0), (11, 30), 3, (2017, 11, 23, 11, 30))
        _assert_earliest_time_equals((2017, 11, 16, 12, 0), (12, 30), 3, (2017, 11, 16, 12, 30))
        _assert_earliest_time_equals((2017, 11, 16, 12, 0), (15, 30), 3, (2017, 11, 16, 15, 30))

        # next Wednesday
        _assert_earliest_time_equals((2017, 11, 16, 12, 0), (9, 0), 2, (2017, 11, 22, 9, 0))
        _assert_earliest_time_equals((2017, 11, 16, 12, 0), (12, 0), 2, (2017, 11, 22, 12, 0))
        _assert_earliest_time_equals((2017, 11, 16, 12, 0), (15, 0), 2, (2017, 11, 22, 15, 0))

        # next Friday
        _assert_earliest_time_equals((2017, 11, 16, 12, 0), (9, 0), 4, (2017, 11, 17, 9, 0))
        _assert_earliest_time_equals((2017, 11, 16, 12, 0), (12, 0), 4, (2017, 11, 17, 12, 0))
        _assert_earliest_time_equals((2017, 11, 16, 12, 0), (15, 0), 4, (2017, 11, 17, 15, 0))


