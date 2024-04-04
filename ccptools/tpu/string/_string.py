__all__ = [
    'str_norm',
    'str_norm_eq',
    'maxlen',
    'slugify',
    'dequote',
]

"""String Related Type Utilities

Utilities for manipulating strings, i.e. the input AND output of functions here
should both only be strings (str and/or unicode).

These should be pretty basic though, e.g. HTML stuff or formatting stuff etc.
should probably live somewhere else.

This should NOT contain functions that:

 - ...take in a string and output something else, e.g. convert or cast a
   string to some other object type (that's "casting").
 - ...take in some other object type and output a string, e.g. to renders
   stuff readable (that's "formatting").
"""
from ccptools.tpu.casting import decode_bytes
from ccptools.tpu.structs import *

_SLUG_SPACER = re.compile(r'[\s_\-:;,.]+')
_SLUGGER = re.compile(r'[^a-z0-9\-]+')


def str_norm(string: Union[str, bytes], default='') -> str:
    """Normalize a string, i.e. ensure that it is indeed a string (if possible)
    and strip leading and trailing whitespaces and make it lowercase.

    Returns a default value if the string is a None or if an exception is
    encountered while trying to turn a non-string into a string via the str()
    method.

    :param string:
    :type string:
    :param default:
    :type default: any
    :return:
    :rtype:
    """
    if isinstance(string, bytes):
        try:
            string = decode_bytes(string)
        except Exception:
            return default

    if not isinstance(string, str):
        if string is None:
            return default
        try:
            string = str(string)
        except Exception:
            return default
    return string.strip().lower()


def str_norm_eq(string, another_string):
    """Checks if two strings are the same if normalized (i.e. stripped of
    leading and trailing whitespaces and made lowercase).

    Returns False if one or both can't be turned into a string.

    :param string:
    :type string:
    :param another_string:
    :type another_string:
    :return:
    :rtype: bool
    """
    string = str_norm(string, default=None)
    another_string = str_norm(another_string, default=None)
    if string is not None and another_string is not None:
        return string == another_string
    return False


def maxlen(string: str, max_length: int) -> str:
    """Trims the back of a string if it exceeds a certain length.

    If the given parameter is not a string, it'll be returned unchanged.

    :param string:
    :type string: str, unicode or any
    :param max_length:
    :type max_length: int
    :return:
    :rtype: str, unicode or any
    """
    if string and isinstance(string, str) and len(string) > max_length:
        string = string[:max_length]
    return string


def slugify(string):
    """Returns a "slug" version of a string (replacing any whitespaces
    and separators with - and removing any character that is not a-z or 0-9)

    :param string:
    :type string:
    :return:
    :rtype:
    """
    string = str_norm(string)
    string = _SLUG_SPACER.sub('-', string)
    return _SLUGGER.sub('', string)


def dequote(string: str, symbol_list: Optional[Union[str, List[str]]] = None) -> str:
    """Removes single or double quote pairs (or any custom given quotation
    character symbold) from a string if it is encompassed.
    in those.

    Example:

    >>> dequote('"foo"')
    'foo'
    >>> dequote("'bar and another bar'")
    'bar and another bar'

    By default only single `'` or double quotes `"` are removed but you can pass
    in a different character symbol or a list of symbols to act as quotes.

    >>> dequote('$foo$', '$')
    'foo'
    >>> dequote('%bar and another bar%', ['%', '$', '"'])
    'bar and another bar'

    The string must start and end with the same type of quote in order for it
    to be removed. In all other cases the same string will be returned unchanged
    (even if the value isn't an actual string').

    >>> dequote('"foo')
    '"foo'
    >>> dequote('%bar and another bar$', ['%', '$', '"'])
    '%bar and another bar$'
    >>> dequote(None)
    None
    >>> dequote(42)
    42

    :param string: String to remove surrounding quotes from
    :type string: str | unicode
    :param symbol_list: A list of symbols that should act as quotes (optional)
    :type symbol_list: None | list | tuple | set | str | unicode
    :return: The string input without surrounding quotes or whatever was passed
             in unchanged.
    :rtype: str | unicode
    """
    if string and isinstance(string, str):
        symbol_list = symbol_list or ('"', "'")
        if not isinstance(symbol_list, (list, tuple, set)):
            symbol_list = [symbol_list]
        if string[0] == string[-1] and string[0] in symbol_list:
            return string[1:-1]
    return string
