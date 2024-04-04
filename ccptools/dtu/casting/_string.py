__all__ = [
    'regex_to_datetime',
    'isostr_to_datetime',
]

from ccptools.dtu.structs import *
from typing import *

_T_PATTERN = Union[re.Pattern, str]

# Rexex from HELL! ;)
_ISODATE_REGEX = re.compile(r'^(?:(?P<year>[0]{0,3}[1-9]\d{0,3})[- /.,\\]'
                            r'(?P<month>1[012]|0?\d)[- /.,\\](?P<day>3[01]|[012]?\d))?'
                            r'(?:[ @Tt]{0,1}(?:(?P<hour>[2][0-3]|[01]?\d)[ .:,]'
                            r'(?P<minute>[012345]?\d))?(?:[ .:,](?P<second>[012345]?\d)'
                            r'(?:[ .:,](?P<millisecond>\d{0,6}))?)?)?')


def regex_to_datetime(string: str, regex_pattern: _T_PATTERN) -> Optional[Datetime]:
    """Given a string and a regex pattern with named groups with the same
    keywords as the datetime object takes, this method uses that pattern to grab
    those keywords and initialize and return a datetime object.

    If only date keywords are found, the resulting datetime will have its time
    set to midnight (0:00:00.0).

    If only time keywords are found, the resulting datetime will have its date
    set to today's date.

    Failing to find a valid pattern this will simply return a None.
    """
    if isinstance(regex_pattern, str):
        regex_pattern = re.compile(regex_pattern)
    match = regex_pattern.match(string.strip())
    if match:
        parts = match.groupdict()
        found_date = False
        if parts['year'] and parts['month'] and parts['day']:
            date_part = Date(int(parts['year']), int(parts['month']), int(parts['day']))
            found_date = True
        else:
            date_part = Date.today()

        found_time = False
        if parts['hour'] and parts['minute']:
            time_part = Time(int(parts['hour']), int(parts['minute']), int(parts['second'] or 0), int(parts['millisecond'] or 0))
            found_time = True
        else:
            time_part = Time()

        if found_date or found_time:
            return Datetime.combine(date_part, time_part)
    return None


def isostr_to_datetime(string: str) -> Optional[Datetime]:
    """Converts an iso(-ish) formatted string to datetime.

    The pattern is quite forgiving in a few ways so context based
    sanity-checking might be in order when parsing strings from "iffy"
    sources (user input):

        - The time part is optional, as well as individual time parts
        - Seperator character for date parts can be: dash (-), slash (/),
          backslash (\\), dot (.), comma (,), or space ( )
        - Seperator character for time parts can be: colum (:), dot (.),
          comma (,), or space ( )
        - Seperator character of date and time halves can be: either case of
          the letter T (T or t), the at symbol (@) or space ( )
        - Values less than ten do not have to be zero-filled
          ("2013-1-2T3:4:5.6789" == "2013-01-02T03:04:05.6789")
        - The year can be any value from 1-9999

    Otherwise, normal datetime restrictions apply (month must be 1-12, minutes
    hust me 0-59 etc.)

    This function is timezone naive.

    Failing to find a valid pattern this will simply return a None.
    """
    return regex_to_datetime(string, _ISODATE_REGEX)
