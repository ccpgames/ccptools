# CCP Games Python Date/Time Utilities

## TL;DR Use

```python
from ccptools import dtu

dt = dtu.Datetime(2023, 8, 27, 13, 37)
```


## Structs

Under the `ccptools.dtu.structs` submodule there are a number of 
useful data structures and type alias that are publicly exported.

### Object Aliases

The classic `datetime` objects have been "renamed" via aliasing in 
`ccptools.dtu` like so:

| Class Alias | Original Class       |
|-------------|----------------------|
| `Date`      | `datetime.date`      |
| `Time`      | `datetime.time`      |
| `Datetime`  | `datetime.datetime`  |
| `TimeDelta` | `datetime.timedelta` |
| `TzInfo`    | `datetime.tzinfo`    |
| `TimeZone`  | `datetime.timezone`  |

This may seem odd at first, especially to seasoned Python veterans who are 
desensitised to the oddities of the `datetime.datetime` class in the `datetime` 
module having the identical name as it's containing module as well as all 
other classes in that module "violating" the PEP 8 guidelines for using 
CapWord names for classes.

The point is simply to make is possible to generate cleaner and more 
readable code with the minimum amount of fuss, without actually changing 
anything important or requiring refactoring or learning new stuff.

Replacing...
```python
import datetime
foo = datetime.datetime(1984, 4, 4)
```
...with... 
```python
from ccptools import dtu
bar = dtu.Datetime(1984, 4, 4)
```

...results in:

- any ambiguity as to what is a class and what is a module is gone
- new Python coders not being confused as hell
- veteran Python coders don't have to learn a new syntax or way of working 
  and thinking, since the only change is the capitalization of one or two 
  characters in the class names
- code reading and "feeling" better _(arguable statement but a stand by it)_
- code being _(or at least looking)_ PEP 8 compliant
- no code breaking since the following still remains `True`:
  - `type(foo) == type(bar)`
  - `foo == bar`
  - This is because `dtu.Datetime` is just an alias of the actual 
    `datetime.datetime` class so using `dtu.Datetime` nevertheless results in 
    a `datetime.datetime` object being generated


### Type Aliases

There are a few typing aliases defined in `ccptools.dtu` (mostly for 
internal use as parameter type annotations and such) but made publicly 
available in case they're useful for anyone else.

| Typing Alias       | Value                                                    |
|--------------------|----------------------------------------------------------|
| `T_DATETIME_VALUE` | `Union[datetime.datetime, datetime.date, datetime.time]` |
| `T_DATE_VALUE`     | `Union[datetime.datetime, datetime.date]`                |
| `T_TIME_VALUE`     | `Union[datetime.datetime, datetime.time]`                |
| `T_TEMPORAL_VALUE` | `Union[T_DATETIME_VALUE, float, int, str, bytes]`        |
| `T_NUMBER`         | `Union[int, float]`                                      |

#### The `T_DATETIME_VALUE` Type Alias

```python
T_DATETIME_VALUE = Union[datetime.datetime, datetime.date, datetime.time]
```

This represents the classic `datetime` data types that can store either a date 
value, a time value or both.

#### The `T_DATE_VALUE` Type Alias

```python
T_DATE_VALUE = Union[datetime.datetime, datetime.date]
```

This represents the classic `datetime` data types that can store a date 
value (so `date` and `datetime`). 

It's use case is mainly where a method needs a date value and can take in 
either one of these, like the `set_midnight()` method. 

#### The `T_TIME_VALUE` Type Alias

```python
T_TIME_VALUE = Union[datetime.datetime, datetime.time]
```

This represents the classic `datetime` data types that can store time 
value (so `time` and `datetime`). 

#### The `T_TEMPORAL_VALUE` Type Alias

```python
T_TEMPORAL_VALUE = Union[datetime.datetime, datetime.date, datetime.time, 
                                float, int, str, bytes]
```

This represents anything that can potentially and reasonably hold a date, 
time or datetime value in various formats.

It's mostly used in the `casting` submodule as type annotation for input 
parameters for various methods that take in differently formatted date 
and/or time values and turn into a Python `datetime.datetime` object, like 
the `any_to_datetime()` method. 

#### The `T_NUMBER` Type Alias

```python
T_NUMBER = typing.Union[int, float]
```

This is just a convenient alias for parameters that can be either integers 
or floating numbers.

### Constants

TODO: Document this

### The `DeltaSplit` Class

TODO: Document this


## Shortcuts

```python
from ccptools import dtu

# Shortcut for `datetime.datetime.now()`
dtu.now()

# Shortcut for `datetime.datetime.now().time()`
dtu.now_time()

# Shortcut for `datetime.date.today()`
dtu.today()

# Shortcut for `time.time()`
dtu.ticks()

# Takes any T_TEMPORAL_VALUE and returns True if it is in the past
# This uses dtu.any_to_datetime for casting
dtu.is_past('2024-04-02T13:47:25')

# Takes any T_TEMPORAL_VALUE and returns True if it is in the future
# This uses dtu.any_to_datetime for casting
dtu.is_future('2024-04-02T13:47:25')

# Find the earlier datetime when the given `find_time` occurs, after an
# optional given `start_dt`, which is the current datetime by default.
dtu.next_time(dtu.Time(11, 0))

# Find the earlier datetime occurrence of the given `day_of_week`
# (where 0 = Monday) after an optional given `start_dt`, which is the current
# datetime by default and using the optional given `find_time`, which is
# midnight by default.
dtu.next_weekday(dtu.Weekday.MONDAY)

# Rounds off any hours, minutes, seconds, etc. of a datetime object and
# sets the time to midnight that day or combines a date object with a time
# object set to midnight.
dtu.set_midnight(dtu.now())

# Adds the given number of weeks, days, hours, minutes and/or seconds
# to the current datetime and returns it.
dtu.from_now(weeks=2)

# Subtracts the given number of weeks, days, hours, minutes and/or seconds
# from the current datetime and returns it.
dtu.ago(days=3)
```

## Casting

```python
from ccptools import dtu

# Turns datetime, date, Windows filetime and posix time into a python
# datetime if possible.
dtu.any_to_datetime('2024-04-02 13:47:25')

# Converts a Windows file time value (number of 100-nanosecond ticks since
# 1 January 1601 00:00:00 UTC) to a standard python datetime.
dtu.filetime_to_datetime(130096156280000100)

# Converts a python datetime (or date) object to a Windows filetime value
# (number of 100-nanosecond ticks since 1 January 1601 00:00:00 UTC).
dtu.datetime_to_filetime(dtu.Datetime(2013, 4, 5, 6, 7, 8, 10))

# Converts an iso(-ish) formatted string to datetime.
dtu.isostr_to_datetime('2024-04-02 13:47:25')

# Given a string and a regex pattern with named groups with the same
# keywords as the datetime object takes, this method uses that pattern to grab
# those keywords and initialize and return a datetime object.
dtu.regex_to_datetime('31/12/2023', r'(?P<day>\d+)/(?P<month>\d+)/(?P<year>\d+)')
```

## Formatting

```python
from ccptools import dtu

# Returns the ISO string version of datetimes, dates, times and the float
# version of total_seconds of timedeltas.
dtu.serialize(dtu.now())

# Returns a string version of whatever serialize returned.
dtu.to_str(dtu.now())

# Turns timedelta into a string like "3 weeks"
# or "a few seconds" or "1 year and 7 months".
dtu.deltastr(dtu.now() - dtu.from_now(days=5))

# Same as deltastr except if given a date/time/datetime value it
# automatically calculates the timedelta from (or to) now to (or from) the
# given value and uses that.
dtu.agostr(dtu.from_now(days=5))
```