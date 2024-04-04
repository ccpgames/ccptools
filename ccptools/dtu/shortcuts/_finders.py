__all__ = [
    'next_time',
    'next_weekday',
    'set_midnight',
    'from_now',
    'ago',
]

from ccptools.dtu.structs import *


def next_time(find_time: Time, start_dt: Optional[Datetime] = None) -> Datetime:
    """Find the earlier datetime when the given `find_time` occurs, after an
    optional given `start_dt`, which is the current datetime by default.

    Useful if you need something like "When does the next happy hour start?" if
    "Happy-Hour" starts at 17:00 every day.

    So if it's 2023-09-02 and 13:23:57...
    >>> next_time(Time(17, 0))
    datetime.datetime(2023, 9, 2, 17, 0, 0, 0)

    But if its past 17, or 2023-09-02 and 19:23:57, we get tomorrow...
    >>> next_time(Time(17, 0))
    datetime.datetime(2023, 9, 3, 17, 0, 0, 0)
    """
    start_dt = start_dt or Datetime.now()
    dt_with_time_replaced = Datetime.combine(start_dt.date(), find_time)
    if dt_with_time_replaced <= start_dt:
        # New time is BEFORE the original time, so move it forward by one day
        dt_with_time_replaced += TimeDelta(days=1)
    return dt_with_time_replaced


def next_weekday(day_of_week: Union[Weekday, int],
                 find_time: Optional[Time] = None,
                 start_dt: Optional[Datetime] = None) -> Datetime:
    """Find the earlier datetime occurrence of the given `day_of_week`
    (where 0 = Monday) after an optional given `start_dt`, which is the current
    datetime by default and using the optional given `find_time`, which is
    midnight by default.
    """
    start_dt = start_dt or Datetime.now()  # Today
    find_time = find_time or Time()  # Midnight
    dt_with_time_replaced = datetime.datetime.combine(start_dt.date(), find_time)
    if dt_with_time_replaced <= start_dt:
        # New time is BEFORE the original time, so move it forward by one day
        dt_with_time_replaced += datetime.timedelta(days=1)

    # Now we need to advance enough days to land on the correct week day
    days_to_advance = (day_of_week - dt_with_time_replaced.weekday()) % 7
    return dt_with_time_replaced + datetime.timedelta(days=days_to_advance)


def set_midnight(dt: T_DATE_VALUE) -> Datetime:
    """Rounds off any hours, minutes, seconds, etc. of a datetime object and
    sets the time to midnight that day or combines a date object with a time
    object set to midnight.
    """
    if isinstance(dt, Datetime):
        dt = dt.date()
    if isinstance(dt, Date):
        return datetime.datetime.combine(dt, Time())
    return dt


def from_now(days: T_NUMBER = 0, hours: T_NUMBER = 0, minutes: T_NUMBER = 0,
             seconds: T_NUMBER = 0, weeks: T_NUMBER = 0) -> Datetime:
    """Adds the given number of weeks, days, hours, minutes and/or seconds
    to the current datetime and returns it.
    """
    return Datetime.now() + TimeDelta(days=days, hours=hours, minutes=minutes, seconds=seconds, weeks=weeks)


def ago(days: T_NUMBER = 0, hours: T_NUMBER = 0, minutes: T_NUMBER = 0,
           seconds: T_NUMBER = 0, weeks: T_NUMBER = 0) -> Datetime:
    """Subtracts the given number of weeks, days, hours, minutes and/or seconds
    from the current datetime and returns it.
    """
    return Datetime.now() - TimeDelta(days=days, hours=hours, minutes=minutes, seconds=seconds, weeks=weeks)
