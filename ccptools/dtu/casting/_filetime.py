__all__ = [
    'filetime_to_datetime',
    'datetime_to_filetime',
]

from ccptools.dtu.structs import *

_FILETIME_NULL_DATE = Datetime(1601, 1, 1, 0, 0, 0)


def filetime_to_datetime(filetime: T_NUMBER) -> Datetime:
    """Converts a Windows file time value (number of 100-nanosecond ticks since
    1 January 1601 00:00:00 UTC) to a standard python datetime.
    Valid values are approx. -5.04911232e17 to 2.65046774399999999e18

    This function is timezone naive.

    :raise OverflowError: if filetime value is out of the range of python
                          datetime (between the year 1 and 9999 AD)
    """
    return _FILETIME_NULL_DATE + TimeDelta(microseconds=(filetime / 10))


def datetime_to_filetime(dt: T_DATE_VALUE) -> int:
    """Converts a python datetime (or date) object to a Windows filetime value
    (number of 100-nanosecond ticks since 1 January 1601 00:00:00 UTC).

    If the supplied parameter is a date as opposed to a datetime, it will first
    be converted locally to a datetime with the time 00:00:00.000000

    This function is timezone naive.
    """
    if not isinstance(dt, Datetime) and isinstance(dt, Date):
        dt = Datetime.combine(dt, Time(0, 0, 0))
    delta = dt - _FILETIME_NULL_DATE
    return 10 * ((delta.days * 86400 + delta.seconds) * 1000000 + delta.microseconds)
