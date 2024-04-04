import unittest
import datetime

from ccptools import dtu


class FindersTest(unittest.TestCase):
    def test_find_earliest_time_and_weekday_after_datetime(self):
        def _assert_earliest_time_equals(start, seek_time_of_day, seek_day_of_week, expected):
            datetime_start = datetime.datetime(*start)
            time_of_day = datetime.time(*seek_time_of_day)
            datetime_expected = datetime.datetime(*expected)

            datetime_result = dtu.next_weekday(seek_day_of_week, time_of_day, datetime_start)

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


