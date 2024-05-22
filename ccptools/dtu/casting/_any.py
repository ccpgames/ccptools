__all__ = [
    'any_to_datetime',
]
import warnings

from ccptools.dtu.structs import *
from ccptools._common import *
from ccptools.dtu.casting._filetime import *
from ccptools.dtu.casting._string import *
from ccptools.dtu.casting._timestamp import *
from ccptools.dtu.casting._instant import *

_NOT_SUPPLIED = object()

_now = Datetime.now()
_1000_years_plus = _now.replace(_now.year + 1000)
_1000_years_minus = _now.replace(_now.year - 1000)

_TIMESTAMP_MIN_RANGE = datetime_to_timestamp(_1000_years_minus)
_TIMESTAMP_MAX_RANGE = datetime_to_timestamp(_1000_years_plus)

_INSTANT_MIN_RANGE = datetime_to_instant(_1000_years_minus)
_INSTANT_MAX_RANGE = datetime_to_instant(_1000_years_plus)

_REVERSE_DATETIME_REXEX = re.compile(r'(?P<day>3[01]|[012]?\d)[- /.,\\](?P<month>1[012]|0?\d)[- /.,\\]'
                                     r'(?P<year>[12][0189]\d{2})(?:[ @Tt]{0,1}(?:(?P<hour>[2][0-3]|[01]?\d)[ .:,]'
                                     r'(?P<minute>[012345]?\d))?(?:[ .:,](?P<second>[012345]?\d)'
                                     r'(?:[ .:,](?P<millisecond>\d{0,6}))?)?)?')
_REVERSE_US_DATETIME_REXEX = re.compile(r'(?P<month>1[012]|0?\d)[- /.,\\](?P<day>3[01]|[012]?\d)[- /.,\\]'
                                        r'(?P<year>[12][0189]\d{2})(?:[ @Tt]{0,1}(?:(?P<hour>[2][0-3]|[01]?\d)[ .:,]'
                                        r'(?P<minute>[012345]?\d))?(?:[ .:,](?P<second>[012345]?\d)'
                                        r'(?:[ .:,](?P<millisecond>\d{0,6}))?)?)?')


def any_to_datetime(temporal_object: T_TEMPORAL_VALUE,
                    default: Any = _NOT_SUPPLIED) -> Union[Datetime, Any]:
    """Turns datetime, date, Windows filetime and posix time into a python
    datetime if possible. By default, returns the same input value on failed
    casting but another default return value can be given.

    This function is timezone naive.

    If given a number the following trickery is performed:

    - If the number, treated as a timestamp, represents a datetime value that is
      within 1000 years of now (past or future) it will be treated as a timestamp
      because timestamps are the most commonly used numerical representations of
      datetimes
    - If the number is outside that range, we'll check if the number would be
      within 1000 years of now if treated as an instant.
    - Otherwise, we assume that such a large number must be a filetime

    This does mean that there are certain cases that will yield incorrect
    results, including:

    - Timestamps more than 1000 years in the past or future (they'll be
      treated as instants or filetimes)
    - Instants within a couple of years of 1970 (1969-01-20 to 1971-01-22 at
      the time of this writing) will be treated as timestamps
    - Filetimes for the years 1600-1601 might get treated as instants or
      timestamps

    Concerning strings, there are also potential pitfalls if casting US
    formatted YYYY-DD-MM strings, as this method will FIRST assume a standard
    ISO format and only try the US one if that fails, so US formatted strings
    with days between 1 and 12 will be treated as ISO and have their day and
    month numbers switched.

    Note: This is a "best-guess" method and if these edge cases are
    unacceptable, you should totally not be using it, and instead, know exactly
    what format your data is in and use the appropriate specific casting method.
    """
    if default == _NOT_SUPPLIED:
        default = temporal_object
    try:
        if isinstance(temporal_object, Datetime):
            return temporal_object

        if isinstance(temporal_object, Date):
            return datetime.datetime.combine(temporal_object, Time())

        if isinstance(temporal_object, (float, int)):
            if _TIMESTAMP_MIN_RANGE < temporal_object < _TIMESTAMP_MAX_RANGE:
                # This range means that the number, if treated as a timestamp,
                # represents a datetime within 1000 years to/from now so it's the
                # most likely bet!
                return timestamp_to_datetime(temporal_object)

            if _INSTANT_MIN_RANGE < temporal_object < _INSTANT_MAX_RANGE:
                # This range means that the number, if treated as an instant,
                # represents a datetime within 1000 years to/from now so it's the
                # second most likely bet!
                return instant_to_datetime(temporal_object)

            # This number is so large that it's most likely a filetime!
            return filetime_to_datetime(temporal_object)

        if isinstance(temporal_object, bytes):
            try:
                temporal_object = decode_bytes(temporal_object)
            except ValueError:
                return temporal_object

        if isinstance(temporal_object, str):
            # Is this a number in string format?
            try:
                # Let's just try and pass this through the int caster, if that works, we evaluate it again as an int
                return any_to_datetime(int(temporal_object))
            except (TypeError, ValueError):
                pass

            try:
                # Let's just try and pass this through the float caster, if that works, we evaluate it again as an int
                return any_to_datetime(float(temporal_object))
            except (TypeError, ValueError):
                pass

            # First we'll try the day-month-year pattern
            value = regex_to_datetime(temporal_object, _REVERSE_DATETIME_REXEX)
            if value:
                return value

            # Then the month-day-year pattern
            value = regex_to_datetime(temporal_object, _REVERSE_US_DATETIME_REXEX)
            if value:
                return value

            # How'bout good old ISO year-month-day then? :D
            value = isostr_to_datetime(temporal_object)
            if value:
                return value

    except (OverflowError, ValueError):
        pass  # Oh well

    return default
