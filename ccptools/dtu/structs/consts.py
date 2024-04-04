__all__ = [
    'DAYS_IN_MEAN_YEAR',
    'DAYS_IN_MEAN_MONTH',
    'DAYS_IN_MEDIAN_YEAR',
    'DAYS_IN_MEDIAN_MONTH',
    'WHOLE_DAYS_IN_MEAN_YEAR',
    'WHOLE_DAYS_IN_MEAN_MONTH',
    'SECONDS_IN_ONE_MINUTE',
    'SECONDS_IN_ONE_HOUR',
    'SECONDS_IN_ONE_DAY',
    'Weekday',
]

import enum

DAYS_IN_MEAN_YEAR = 365.2425  # Every 400 years we get 97 leap years (303*365 + 97*366)/400
DAYS_IN_MEAN_MONTH = 30.436875  # Mean Year / 12
DAYS_IN_MEDIAN_YEAR = 365  # Most common value (303 vs. 97 per 400 year cycle)
DAYS_IN_MEDIAN_MONTH = 31  # Most common value (7 out of 12)
WHOLE_DAYS_IN_MEAN_YEAR = 365
WHOLE_DAYS_IN_MEAN_MONTH = 30

SECONDS_IN_ONE_MINUTE = 60
SECONDS_IN_ONE_HOUR = 3600  # 60 * 60
SECONDS_IN_ONE_DAY = 86400  # 60 * 60 * 24


class Weekday(enum.IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6
