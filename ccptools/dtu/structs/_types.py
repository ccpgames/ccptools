__all__ = [
    'T_DATETIME_VALUE',
    'T_DATE_VALUE',
    'T_TIME_VALUE',
    'T_TEMPORAL_VALUE',
    'T_NUMBER',
]

from ccptools.dtu.structs._base import *

# Any datetime value
T_DATETIME_VALUE = Union[datetime.datetime, datetime.date, datetime.time]

# Containing a date
T_DATE_VALUE = Union[datetime.datetime, datetime.date]

# Containing time
T_TIME_VALUE = Union[datetime.datetime, datetime.time]

# Any type that can possibly contain a date and/or time value
T_TEMPORAL_VALUE = Union[T_DATETIME_VALUE, float, int, str, bytes]

# Number
T_NUMBER = Union[int, float]
