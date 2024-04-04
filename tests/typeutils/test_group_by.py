import unittest
from ccptools.tpu import iters

import datetime


lennon = datetime.date(1940, 10, 9)  # John Lennon: October 9, 1940
mccartney = datetime.date(1942, 6, 18)  # Paul McCartney: June 18, 1942
harrison = datetime.date(1943, 2, 25)  # George Harrison: February 25, 1943
starr = datetime.date(1940, 7, 7)  # Ringo Starr: July 7, 1940
jagger = datetime.date(1943, 7, 26)  # Mick Jagger: July 26, 1943
richards = datetime.date(1943, 10, 18)  # Keith Richards: December 18, 1943
watts = datetime.date(1941, 6, 2)  # Charlie Watts (who was the drummer until his passing in 2021): June 2, 1941
wood = datetime.date(1947, 6, 1)  # Ronnie Wood: June 1, 1947
jones = datetime.date(1942, 2, 28)  # Brian Jones (original member, until his death in 1969): February 28, 1942
wyman = datetime.date(1936, 8, 24)  # Bill Wyman (member from 1962 until 1993): October 24, 1936


class GroupByTest(unittest.TestCase):
    def test_by_year(self):
        list_of_dates = [
            lennon,
            mccartney,
            harrison,
            starr,
            jagger,
            richards,
            watts,
            wood,
            jones,
            wyman,
        ]

        expected_grouping_by_year = {
            1940: [lennon, starr],
            1942: [mccartney, jones],
            1943: [harrison, jagger, richards],
            1941: [watts],
            1947: [wood],
            1936: [wyman]
        }

        self.assertEqual(expected_grouping_by_year, iters.group_by(list_of_dates, 'year'))

    def test_by_weekday(self):
        list_of_dates = [
            lennon,
            mccartney,
            harrison,
            starr,
            jagger,
            richards,
            watts,
            wood,
            jones,
            wyman,
        ]
        expected_grouping_by_weekday = {
            2: [lennon],
            3: [mccartney, harrison],
            6: [starr, wood],
            0: [jagger, richards, watts, wyman],
            5: [jones]
        }
        self.assertEqual(expected_grouping_by_weekday, iters.group_by(list_of_dates, 'weekday'))

    def test_by_last_letter(self):
        list_of_names = [
            'lennon',
            'mccartney',
            'harrison',
            'starr',
            'jagger',
            'richards',
            'watts',
            'wood',
            'jones',
            'wyman',
        ]

        expected_grouping_by_letter = {
            'n': ['lennon', 'harrison', 'wyman'],
            'y': ['mccartney'],
            'r': ['starr', 'jagger'],
            's': ['richards', 'watts', 'jones'],
            'd': ['wood']
        }

        self.assertEqual(expected_grouping_by_letter, iters.group_by(list_of_names, -1))
