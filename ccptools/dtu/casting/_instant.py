__all__ = [
    'instant_to_datetime',
    'datetime_to_instant',
]
from ccptools.dtu.structs import *
from ._timestamp import *


def instant_to_datetime(milliseconds_since_epoch: T_NUMBER, minmax_on_fail: bool = False) -> Datetime:
    """Converts an integer representing milliseconds since the Unix epoch
    (January 1, 1970) to a Python datetime object.

    :param milliseconds_since_epoch: Milliseconds since Unix epoch (January 1, 1970).
    :param minmax_on_fail: If True, will return the minimum or maximum possible
                           value of Datetime in case of overflow (positive or
                           negative)
    :return: A Python Datetime
    """
    return timestamp_to_datetime(milliseconds_since_epoch / 1000., minmax_on_fail)


def datetime_to_instant(dt: T_DATE_VALUE) -> int:
    """Converts a Python datetime object to the number of milliseconds since
    Unix epoch (January 1, 1970).

    If given a date only, it will assume a time of 00:00:00.000000.

    :param dt: Python datetime (or date).
    :return: Number of milliseconds since Unix epoch (January 1, 1970)
    """
    return int(datetime_to_timestamp(dt) * 1000)
