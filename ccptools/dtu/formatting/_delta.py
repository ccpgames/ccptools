__all__ = [
    'deltastr',
    'agostr',
]

from ccptools.dtu.structs import *


def deltastr(delta: TimeDelta, default: str = '') -> str:
    """Turns timedelta into a string like "3 weeks"
    or "a few seconds" or "1 year and 7 months".

    Example:

        >>> deltastr(datetime.timedelta(days=2002, seconds=20000))
        '5 years'
        >>> deltastr(datetime.timedelta(days=366, seconds=20000))
        '1 year and 5 hours'
        >>> deltastr(datetime.timedelta(seconds=360))
        '6 minutes'
        >>> deltastr(datetime.timedelta(seconds=90))
        '1 minute'
        >>> deltastr(datetime.timedelta(seconds=59))
        'a few seconds'
    """
    if not isinstance(delta, TimeDelta):
        return default

    ds = DeltaSplit(delta)
    return ds.to_str(max_number_of_fields=2,
                     include_seconds=False,
                     directionals=None,
                     only_sec_str='a few seconds',
                     granularity_halting_threshold=1)


def agostr(delta_or_date: Union[T_DATETIME_VALUE, TimeDelta], default: str = '', utc: bool = True) -> str:
    """Same as deltastr except if given a date/time/datetime value it
    automatically calculates the timedelta from (or to) now to (or from) the
    given value and uses that.

    This function uses UTC time for comparison by default but can be instructed
    to use the local timezone of its running environment.
    """
    if utc:
        now = Datetime.utcnow()
    else:
        now = Datetime.now()

    if isinstance(delta_or_date, Datetime):
        delta_or_date = now - delta_or_date

    elif isinstance(delta_or_date, Date):
        delta_or_date = now.date() - delta_or_date

    elif isinstance(delta_or_date, Time):
        delta_or_date = Datetime.combine(now.date(), delta_or_date)

    return deltastr(delta_or_date, default)



