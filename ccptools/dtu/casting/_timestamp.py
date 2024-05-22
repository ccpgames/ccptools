__all__ = [
    'timestamp_to_datetime',
    'datetime_to_timestamp',
]
from ccptools.dtu.structs import *
import calendar


def timestamp_to_datetime(seconds_since_epoch: T_NUMBER, minmax_on_fail: bool = False) -> Datetime:
    """Converts an int or float representing seconds since the Unix epoch
    (January 1, 1970) to a Python datetime object.

    :param seconds_since_epoch: Seconds since Unix epoch (January 1, 1970).
    :param minmax_on_fail: If True, will return the minimum or maximum possible
                           value of Datetime in case of overflow (positive or
                           negative)
    :return: A Python Datetime
    """
    try:
        return Datetime.fromtimestamp(seconds_since_epoch)
    except OSError:
        try:
            return Datetime(1970, 1, 1, 0, 0, 0, 0) + TimeDelta(seconds=seconds_since_epoch)
        except OverflowError:
            if minmax_on_fail:
                if seconds_since_epoch > 0:
                    return Datetime.max
                else:
                    return Datetime.min
            else:
                raise


def datetime_to_timestamp(dt: T_DATE_VALUE) -> float:
    """Converts a Python datetime object to the number of seconds since
    Unix epoch (January 1, 1970) as a float, including fractional seconds.

    If given a date only, it will assume a time of 00:00:00.000000.

    :param dt: Python datetime (or date).
    :return: Number of seconds since Unix epoch (January 1, 1970)
    """
    if not isinstance(dt, Datetime) and isinstance(dt, Date):
        dt = Datetime.combine(dt, Time(0, 0, 0, 0))
        # TODO(thordurm@ccpgames.com>) 2024-05-22: HANDLE SECONDS!!!

    int_part = float(calendar.timegm(dt.utctimetuple()))
    if dt.microsecond:
        int_part += dt.microsecond / 1000000.0
    return int_part
