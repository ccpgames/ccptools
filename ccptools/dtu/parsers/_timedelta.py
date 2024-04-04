__all__ = [
    'str_to_delta',
]
from ccptools.dtu.structs import *

_PERIOD_PART = re.compile(r"([+-]?(?:\d+(?:\.(?:\d+)?)?|\.\d+))\s*([a-z]+)\s*", re.IGNORECASE)

_KEYWORDS = {
    'd': 'days',
    'day': 'days',
    'days': 'days',

    'h': 'hours',
    'hr': 'hours',
    'hrs': 'hours',
    'hour': 'hours',
    'hours': 'hours',

    'm': 'minutes',
    'i': 'minutes',
    'min': 'minutes',
    'mins': 'minutes',
    'minute': 'minutes',
    'minutes': 'minutes',

    's': 'seconds',
    'sec': 'seconds',
    'secs': 'seconds',
    'second': 'seconds',
    'seconds': 'seconds',

    'w': 'weeks',
    'wk': 'weeks',
    'wks': 'weeks',
    'week': 'weeks',
    'weeks': 'weeks',
}


def _parse_split(string: str) -> Optional[List[Tuple[str, str]]]:
    """Splits a string presumed to containing a written out time period into a
    list of 2-tuples, each containing a numerical value first in string format
    and then a unit keyword.

    Strictly speaking this just searches for any number in a text (integer or
    decimal, with an optional leading + or -) and the first word following that
    number and pairs them up, but that basically does the job shockingly well.

    Examples:
        >>> _parse_split('2 days 7 hours 10 minutes')
        [('2', 'days'), ('7', 'hours'), ('10', 'minutes')]

        >>> _parse_split('2 days, 7.3 hours and 10 minutes')
        [('2', 'days'), ('7.3', 'hours'), ('10', 'minutes')]

        >>> _parse_split('2 days, 7.3 hrs and 10 mins')
        [('2', 'days'), ('7.3', 'hrs'), ('10', 'mins')]

        >>> _parse_split('2 days, -7.3 hrs and 10 floops')
        [('2', 'days'), ('-7.3', 'hrs'), ('10', 'floops')]

        >>> _parse_split('2d-7.3h10m')
        [('2', 'd'), ('-7.3', 'h'), ('10', 'm')]

        >>> _parse_split('1st of all, the 3 bears were really just 2 and-a-half bears')
        [('1', 'st'), ('3', 'bears'), ('2', 'and')]
    """
    if string and isinstance(string, str):
        buf = []
        string = string.strip().lower()
        for match in _PERIOD_PART.finditer(string):
            buf.append(match.groups())
        return buf or None
    return None


def _timedelta_keywords(list_of_lists: List[Tuple[str, str]]) -> Dict:
    """Given a list of 2-tuples, containing the numerical value first in string
    format and then a time unit keyword, parses the numerical value to a Python
    float and changes any time unit format alias or shorthand into its
    equivalent keyword that's a valid argument for initialising a timedelta,
    and then pairs up each of those into a dict that can then be fed into
    timedelta's __init__ as kwargs via the ** operator.

    :raises KeyError: If a time unit keyword was not recognised
    """
    kw_map = {}
    for num, kw in list_of_lists:
        kw_map[_KEYWORDS[kw]] = float(num)
    return kw_map


def split_delta(delta, include_weeks=True, include_months=True, include_years=True):
    """Splits a timedelta into the time periods it approximately
    contains. Mean length of years and months are used and fractional
    days/seconds might get shaved of but this is useful to evaluate individual
    period lengths of displaying the maximum chunk of period a timedelta
    contains.

    This class includes an `is_past` property which is True if the timedelta
    contained a negative value but all the values in the split are nevertheless
    kept positive.

    It also includes a few `largest` and `second_largest` properties that
    contain the first and second period units that contain values greater than 0
    in order of increasing accuracy (i.e. from year to second).

    Example:

        >>> total = datetime.timedelta(days=2002, seconds=20000)
        >>> parts = split_delta(total)
        >>> parts
        {'seconds': 20, 'months': 5, 'days': 2, '2nd': 'months', 'hours': 5, '1st': 'years', 'is_past': False, 'weeks': 3, 'years': 5, 'minutes': 33}

    :param delta: Time period to evaluate
    :type delta: datetime.timedelta
    :param include_weeks: Include weeks in the division (and reduce the days accordingly)?
    :type include_weeks: bool
    :rtype: dict
    """
    ds = DeltaSplit(time_delta=delta, include_weeks=include_weeks, include_months=include_months, include_years=include_years)
    parts = ds.to_dict()
    parts['1st'] = parts.pop('largest')
    parts['2nd'] = parts.pop('second_largest')
    return parts



def str_to_delta(string: str, default: Any = 0) -> Union[TimeDelta, Any]:
    """Converts a simple string with time duration keywords into a
    `datetime.timedelta` object, akin to the keyword arguments in
    `datetime.timedelta`.

    Examples:
    >>> str_to_delta('12days') == datetime.timedelta(days=12)
    True
    >>> str_to_delta('2h34m') == datetime.timedelta(hours=2, minutes=34)
    True
    >>> str_to_delta('-1.5 hours') == datetime.timedelta(hours=-1.5)
    True

    Valid keywords (and aliases):
     - days (d, day)
     - hours (h, hr, hrs, hour)
     - minutes (m, i, min, mins, minute)
     - seconds (s, sec, secs, second)
     - weeks (w, wk, wks, week)

    Numeric values can be integers or floats (with or without a plus or minus
    sign) and all whitespaces are valid but ignored.
    """
    if default == 0:
        default = TimeDelta(seconds=0)
    res = _parse_split(string)
    if res:
        try:
            return TimeDelta(**_timedelta_keywords(res))
        except (ValueError, KeyError, IndexError):
            return default
    else:
        return default
