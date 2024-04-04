__all__ = [
    'float_eval',
    'int_eval',
    'bool_eval',
]
from ccptools.tpu.structs import *
from ccptools._common import decode_bytes  # noqa

_AFFIRMATIVE = {
    'active',
    'enable',
    'enabled',
    'on',
    'true',
    'yes',
    'y',
}


def float_eval(value: Any, default: Union[float, None] = 0.0, raise_on_fail: bool = False) -> Union[float, None]:
    """Safe evaluation of any type to a float value. The optional default value
    will be returned on any parsing or casting error. You can also pass None as
    the default to check for failures.

    Adding the raise_on_fail parameter and setting it to True will cause the
    method to raise TypeError or ValueError exceptions if it fails to evaluate a
    float value from the value given.

    Useful shortcut where you have a string that you're know is a float value
    in string form like prefs entries, DB entries from varchar fields or HTTP
    GET/POST arguments

    :type value: any
    :type default: float or None
    :type raise_on_fail: bool
    :rtype: float or None
    """
    if isinstance(value, float):
        return value  # Duh!
    elif isinstance(value, int):
        return float(value)
    elif isinstance(value, (str, bytes)):
        try:
            return float(value)
        except (TypeError, ValueError) as ex:
            if raise_on_fail:
                raise
            return default
    elif isinstance(value, datetime.timedelta):
        return value.total_seconds()
    elif isinstance(value, datetime.date):  # datetime.datetime extends datetime date
        return time.mktime(value.timetuple())
    elif isinstance(value, datetime.time):
        return float(value.hour * 3600 + value.minute * 60 + value.second + value.microsecond * 0.000001)
    else:
        try:
            # Let's just try and pass this through the float caster...?
            return float(value)
        except (TypeError, ValueError):
            pass

        if raise_on_fail:
            raise TypeError(f'Could not evaluate unknown type [{type(value)}] to a float value')
        return default


def int_eval(value: Any, default: Union[int, None] = 0, raise_on_fail: bool = False) -> Union[int, None]:
    """Safe evaluation of any type to an int value. The optional default value
    will be returned on any parsing or casting error. You can also pass None as
    the default to check for failures.

    Long values that contain values larger than ints can contain (or strings
    containing such values) will evaluate to a long.

    Useful shortcut where you have a string that you're know is an int value
    in string form like prefs entries, DB entries from varchar fields or HTTP
    GET/POST arguments

    :type value: any
    :type default: int or None
    :type raise_on_fail: bool
    :rtype: int or long or None
    """
    if isinstance(value, int):
        return value  # Duh!

    elif isinstance(value, float):
        return int(value)

    elif isinstance(value, bytes):
        try:
            value = decode_bytes(value)
        except UnicodeError as ex:
            if raise_on_fail:
                raise
            return default

    if isinstance(value, str):
        try:
            if '.' in value:
                return int(float(value))

            elif value.startswith('0') or value.startswith('-0'):
                return int(value, base=0)

            return int(value)

        except (TypeError, ValueError):
            return default

    elif isinstance(value, datetime.timedelta):
        return int(value.total_seconds())

    elif isinstance(value, datetime.date):  # datetime.datetime extends datetime date
        return int(time.mktime(value.timetuple()))

    elif isinstance(value, datetime.time):
        return int(value.hour * 3600 + value.minute * 60 + value.second)

    else:
        try:
            # Let's just try and pass this through the float caster...?
            return int(value)
        except (TypeError, ValueError):
            pass

    if raise_on_fail:
        raise TypeError(f'Could not evaluate unknown type [{type(value)}] to an int value')

    return default


def bool_eval(value: Any, raise_on_fail: bool = False) -> bool:
    """Evaluates if a value should be interpreted as a boolean True value.
    That means a string that is "True" (or other explicit affirmative words)
    regardless of case and whitespace characters as well as any numerical value
    other than 0 and of course a boolean type of true.

    Anything else returns False, including all objects.

    Boolean types are return their same value.

    Strings and bytes with the following values will (case insensitive) evaluate to True:
    - active
    - enable
    - enabled
    - on
    - true
    - yes
    - y

    Strings and unicode strings that are longs, integers or floats evaluate to
    the same as their "pure" types (int, float) would evaluate to.

    Longs, Integers and Floating number evaluate to False if they are 0L, 0 and
    0.0 respectively, anything else is True.

    Any other type or object yield a False return (the opposite of what Python
    does by default, because we're looking for explicit statements of "Yes!")

    Very useful for evaluating values read from prefs.ini that can use
    different formats.

    :type value: any
    :type raise_on_fail: bool
    :rtype: bool
    """
    if isinstance(value, bool):
        return value  # Duh!

    if isinstance(value, bytes):
        try:
            value = decode_bytes(value)
        except ValueError as ex:
            if raise_on_fail:
                raise
            return False

    if isinstance(value, str):
        value = value.strip().lower()
        if value in _AFFIRMATIVE:
            return True

        elif value.isdigit():
            return bool(int(value))

        else:
            neg = False
            if value.startswith('-'):
                value = value[1:]
                neg = True
                if value.isdigit():
                    return bool(-int(value))
            parts = value.split('.')
            if len(parts) == 2:
                if parts[0].isdigit() and parts[1].isdigit():
                    if neg:
                        return bool(-float(value))
                    else:
                        return bool(float(value))
            return False
    elif isinstance(value, (int, float)):
        return bool(value)
    else:
        return False

