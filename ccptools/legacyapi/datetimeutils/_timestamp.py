__all__ = [
    'datetime_to_timestamp',
]


from ccptools.dtu.structs import *
import time


def datetime_to_timestamp(dt: T_DATE_VALUE) -> int:
    """Silly legacy stuff since this whole thing can more or less be replaced
    with the `timestamp()` method of the `datetime` class (adding and `int()`
    cast if needed).

    :type dt: datetime.datetime | datetime.date
    :rtype: int
    """
    if not isinstance(dt, datetime.datetime) and isinstance(dt, datetime.date):
        dt = datetime.datetime.combine(dt, datetime.time(0, 0, 0))

    return int(time.mktime(dt.timetuple()))
