__all__ = [
    'any_to_datetime',
]

from ccptools.dtu.structs import *
from ccptools._common import *
from ccptools.dtu.casting._filetime import *
from ccptools.dtu.casting._string import *


_NOT_SUPPLIED = object()
_FILETIME_THRESHOLD = 29999999999

_REVERSE_DATETIME_REXEX = re.compile(r'(?P<day>3[01]|[012]?\d)[- /.,\\](?P<month>1[012]|0?\d)[- /.,\\]'
                                     r'(?P<year>[12][0189]\d{2})(?:[ @Tt]{0,1}(?:(?P<hour>[2][0-3]|[01]?\d)[ .:,]'
                                     r'(?P<minute>[012345]?\d))?(?:[ .:,](?P<second>[012345]?\d)'
                                     r'(?:[ .:,](?P<millisecond>\d{0,6}))?)?)?')
_REVERSE_US_DATETIME_REXEX = re.compile(r'(?P<month>1[012]|0?\d)[- /.,\\](?P<day>3[01]|[012]?\d)[- /.,\\]'
                                        r'(?P<year>[12][0189]\d{2})(?:[ @Tt]{0,1}(?:(?P<hour>[2][0-3]|[01]?\d)[ .:,]'
                                        r'(?P<minute>[012345]?\d))?(?:[ .:,](?P<second>[012345]?\d)'
                                        r'(?:[ .:,](?P<millisecond>\d{0,6}))?)?)?')


def any_to_datetime(temporal_object: T_TEMPORAL_VALUE,
                    default: Any = _NOT_SUPPLIED,
                    utc: bool = True) -> Union[Datetime, Any]:
    """Turns datetime, date, Windows filetime and posix time into a python
    datetime if possible. By default, returns the same input value on failed
    casting but another default return value can be given.

    This function is mostly timezone naive, but it can be instructed to correct
    for the local timezone in cases where it gets a UNIX timestamp and
    generates a datetime object from that. The default behaviour is to use UTC.
    """
    if default == _NOT_SUPPLIED:
        default = temporal_object
    try:
        if isinstance(temporal_object, Datetime):
            return temporal_object
        if isinstance(temporal_object, Date):
            return datetime.datetime.combine(temporal_object, Time())
        if isinstance(temporal_object, (float, int)):
            if temporal_object > _FILETIME_THRESHOLD:  # Most likely Windows FILETIME
                return filetime_to_datetime(temporal_object)
            else:  # Might be Unix timestamp
                if utc:
                    return Datetime.utcfromtimestamp(temporal_object)
                else:
                    return Datetime.fromtimestamp(temporal_object)

        if isinstance(temporal_object, bytes):
            try:
                temporal_object = decode_bytes(temporal_object)
            except ValueError:
                return temporal_object

        if isinstance(temporal_object, str):
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
