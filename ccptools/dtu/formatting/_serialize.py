__all__ = [
    'serialize',
    'to_str',
]

from ccptools.dtu.structs import *


def serialize(temporal_object: T_TEMPORAL_VALUE) -> Union[str, float]:
    """Returns the ISO string version of datetimes, dates, times and the float
    version of total_seconds of timedeltas.

    If the given value is none of these, the same value is just returned
    """
    if isinstance(temporal_object, (Datetime, Date, Time)):
        return temporal_object.isoformat()
    elif isinstance(temporal_object, TimeDelta):
        return temporal_object.total_seconds()
    else:
        return temporal_object


def to_str(temporal_object: T_TEMPORAL_VALUE) -> str:
    """Returns a string version of whatever serialize returned.
    """
    return str(serialize(temporal_object))
