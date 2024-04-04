import unittest

from ccptools import dtu


class DeltaSplitTest(unittest.TestCase):
    def test_delta_split(self):
        def assert_output(delta, expected):
            self.assertEqual(expected, dtu.DeltaSplit(delta).to_str(max_number_of_fields=7,
                                                                    include_seconds=True,
                                                                    granularity_halting_threshold=None))

        assert_output(dtu.TimeDelta(seconds=59), 'in 59 seconds')
        assert_output(dtu.TimeDelta(seconds=-90), '1 minute and 30 seconds ago')
        assert_output(dtu.TimeDelta(seconds=360), 'in 6 minutes')
        assert_output(dtu.TimeDelta(days=366, seconds=20000), 'in 1 year, 5 hours, 33 minutes and 20 seconds')  # 1y, 5h, 33m, 20s
        assert_output(-dtu.TimeDelta(days=2002, seconds=20000), '5 years, 5 months, 3 weeks, 2 days, 5 hours, 33 minutes and 20 seconds ago')