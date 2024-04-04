__all__ = [
    'Date',
    'Time',
    'Datetime',
    'TimeDelta',
    'TzInfo',
    'TimeZone',
]
from ccptools.dtu.structs._base import *

# Aliases to "standard" PEP 8 class names. This is to increase readability and
# reduce confusion related to the fact that the most commonly used class/object
# shared the name of its own module (i.e. `datetime.datetime`)
Date = datetime.date
Time = datetime.time
Datetime = datetime.datetime
TimeDelta = datetime.timedelta
TzInfo = datetime.tzinfo
TimeZone = datetime.timezone


