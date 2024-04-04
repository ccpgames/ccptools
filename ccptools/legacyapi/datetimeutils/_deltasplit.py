__all__ = [
    'split_delta',
]

from ccptools import dtu
from ccptools.dtu.structs import *


def split_delta(delta: dtu.TimeDelta, include_weeks: bool = True, include_months: bool = True, include_years: bool = True) -> Dict:
    """Splits a timedelta into a dictionary of time periods it aproximately
    contains. Mean length of years and months are used and fractional
    days/seconds might get shaved of but this is useful to evaluate individual
    period lengths of displaying the maximum chunk of period a timedelta
    contains.

    The dict includes a 'is_past' key in the returned dict which is True if
    the timedelta contained a negative value but all the values in the split
    dict are positive.

    It also includes a '1st' and '2nd' keys that contain the first and second
    keys that contain values greater than 0 in order of increasing accuracy
    (i.e. from year to second).

    Example:

        >>> total = datetime.timedelta(days=2002, seconds=20000)
        >>> parts = split_delta(total)
        >>> parts
        {'seconds': 20, 'months': 5, 'days': 2, '2nd': 'months', 'hours': 5, '1st': 'years', 'is_past': False, 'weeks': 3, 'years': 5, 'minutes': 33}

    :param delta: Time period to evaluate
    :type delta: datetime.timedelta
    :param include_weeks: Include weeks in the division (and reduce the days accordingly)?
    :type include_weeks: bool
    :param include_months: Include months in the division (and reduce the days accordingly)?
    :type include_months: bool
    :param include_years: Include years in the division (and reduce the days accordingly)?
    :type include_years: bool
    :rtype: dict
    """
    parts = dtu.DeltaSplit(time_delta=delta,
                           include_weeks=include_weeks,
                           include_months=include_months,
                           include_years=include_years).to_dict()
    parts['1st'] = parts.pop('largest')
    parts['2nd'] = parts.pop('second_largest')
    return parts
