__all__ = [
    'find_earliest_time_after_datetime',
    'find_earliest_time_and_weekday_after_datetime',
    'date_from_now',
    'date_ago',
]
from ccptools import dtu
from ccptools.dtu.structs import *


def find_earliest_time_after_datetime(dt: Datetime, time: Time) -> Datetime:
    """Alias for `ccptools.dtu.next_time` (with arguments swapped)
    """
    return dtu.next_time(find_time=time, start_dt=dt)


def find_earliest_time_and_weekday_after_datetime(dt: Datetime, time_of_day: Time, day_of_week: Union[Weekday, int]) -> Datetime:
    """Alias for `ccptools.dtu.next_weekday` (with arguments swapped around somewhat)
    """
    return dtu.next_weekday(day_of_week=day_of_week,
                            find_time=time_of_day,
                            start_dt=dt)


def date_from_now(days: int = 0, weeks: int = 0) -> Date:
    return dtu.from_now(days=days, weeks=weeks).date()


def date_ago(days: int = 0, weeks: int = 0) -> Date:
    return dtu.ago(days=days, weeks=weeks).date()
