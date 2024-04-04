"""
This module provides an API to the `ccptools.dtu` (new Date-Time Utils module)
that is backwards compatible with version 2.3.0.0 of the old `datetimeutils`
module.

This is done to facilitate the updating of code that uses `datetimeutils` to use
`ccptools` without requiring too much refactoring.

In most cases where code used something like:
```python
import datetimeutils
```

One should be able to simply replace that line with:
```python
from ccptools.legacyapi import datetimeutils
```

And that should just work.
"""
__all__ = [
    'str_to_timedelta',

    'filetime_to_datetime',
    'datetime_to_filetime',

    'datetime_to_timestamp',

    'regex_to_datetime',
    'isostr_to_datetime',
    'any_to_datetime',

    'split_delta',

    'deltastr',

    'ago',

    'find_earliest_time_after_datetime',
    'find_earliest_time_and_weekday_after_datetime',

    'dt_midnight',
    'dt_from_now',
    'dt_ago',
    'date_from_now',
    'date_ago',

    'str_to_relative_datetime',
    'str_to_2dates',

    'serialize',
    'to_str',
]


from ccptools.dtu import str_to_delta as str_to_timedelta

from ccptools.dtu import filetime_to_datetime
from ccptools.dtu import datetime_to_filetime

from ._timestamp import datetime_to_timestamp

from ccptools.dtu import regex_to_datetime
from ccptools.dtu import isostr_to_datetime

from ccptools.dtu import any_to_datetime

from ._deltasplit import split_delta

from ccptools.dtu import deltastr

from ccptools.dtu import agostr as ago

from ._find import find_earliest_time_after_datetime
from ._find import find_earliest_time_and_weekday_after_datetime

from ccptools.dtu import set_midnight as dt_midnight
from ccptools.dtu import from_now as dt_from_now
from ccptools.dtu import ago as dt_ago

from ._find import date_from_now
from ._find import date_ago

from ccptools.dtu import str_to_rel as str_to_relative_datetime
from ccptools.dtu import str_to_2dates

from ccptools.dtu import serialize
from ccptools.dtu import to_str
