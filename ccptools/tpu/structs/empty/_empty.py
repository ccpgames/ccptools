__all__ = [
    'Empty',
    'EmptyDict',
    'if_empty',
]

import collections


class _Empty(object):
    """
    This is essentially just a glorified None that tries not to break any code
    that makes certain wild assumptions.

    The typical use case here would be to return Empty instead of None as a
    default value for something not found so you don't have to check again and
    again if you got a "None" before calling an attribute so as to not raise
    an AttributeError as long as you don't care if the results of whatever
    you're doing don't make sense until later.

    Totally made up use case example:

    character = get_character(123)
    if character:
        if hasattr(character, 'user'):
            user = character.user
            if user:
                if hasattr(user, 'email'):
                    email = user.email
                    if email:
                        if isinstance(email, (str, unicode)):
                            if email.startswith('_'):
                                raise ValueError('Emails can not start with underscores')

    Totally made up example using Empty as default values for failed lookups:

    if get_character(123).user.email.startswith('_'):
        raise ValueError('Emails can not start with underscores')

    Here get_character returns Empty when it failed to find a character so the
    attribute 'user' of Empty will also return Empty.

    Ditto for the 'email' attribute of 'user'.

    The 'startswith' of 'email' will also be Empty and that will call the
    Empty.__call__('_') which ALSO return Empty and then finally the if
    statement will call Empty.__nonzero__() which returns False.

    So we can super quickly make sure the email doesn't start with an
    underscore IF that's the only thing we care about and don't mind if any
    of the stuff in that chain failed or wasn't found.

    After all, we can always check later explicitly for the validity of any
    and/or all of these attributes.

    Another super simple use case (and probably more likely) would be to use this for quick "throwaway" lookups:

    E.g. printing the domain of the email address of the example above:

    print 'Email:', character.user.email[character.user.email.index('@')+1:]

    If everything was found here, we'll get:
    "Email: ccpgames.com"

    If not, we'll get:
    "Email: Empty"

    Could also do this:
    print 'Email:', character.user.email[character.user.email.index('@')+1:] or '-'
    "Email: -"
    """
    ___inst = None

    def __new__(cls, *args, **kwargs):
        if cls.___inst is None:
            cls.___inst = super(_Empty, cls).__new__(cls, *args, **kwargs)
        return cls.___inst

    def __cmp__(self, other):
        if other is Empty:
            return 0
        return -1

    def __lt__(self, other):
        return False

    def __gt__(self, other):
        return False

    def __le__(self, other):
        if other is Empty:
            return True
        return False

    def __ge__(self, other):
        if other is Empty:
            return True
        return False

    def __eq__(self, other):
        if other is Empty:
            return True
        return False

    def __ne__(self, other):
        if other is Empty:
            return False
        return True

    def __nonzero__(self):
        return False

    def __getattr__(self, name):
        return Empty

    def __setattr__(self, name, value):
        pass

    def __delattr__(self, name):
        pass

    def __instancecheck__(self, instance):
        return False

    def __subclasscheck__(self, subclass):
        return False

    def __str__(self):
        return 'Empty'

    def __unicode__(self):
        return u'Empty'

    def __repr__(self):
        return '<Empty>'

    def __call__(self, *args, **kwargs):
        return Empty

    def __len__(self):
        return 0

    def __getitem__(self, key):
        return Empty

    def __contains__(self, item):
        return False

    def __missing__(self, key):
        return Empty

    def __int__(self):
        return 0

    def __float__(self):
        return 0.0

    def __complex__(self):
        return complex(0, 0)

    def __oct__(self):
        return 00

    def __hex__(self):
        return 0x0

    def __index__(self):
        return 0

    def __trunc__(self):
        return 0

    def __format__(self, formatstr):
        return 'Empty'

    def __pos__(self):
        return Empty

    def __neg__(self):
        return Empty

    def __abs__(self):
        return Empty

    def __invert__(self):
        return Empty

    def __round__(self, n):
        return Empty

    def __floor__(self):
        return Empty

    def __ceil__(self):
        return Empty

    def __copy__(self):
        return Empty

    def __deepcopy__(self):
        return Empty

    def __add__(self, other):
        return Empty

    def __radd__(self, other):
        return Empty

    def __sub__(self, other):
        return Empty

    def __rsub__(self, other):
        return Empty

    def __mul__(self, other):
        return Empty

    def __rmul__(self, other):
        return Empty

    def __floordiv__(self, other):
        return Empty

    def __rfloordiv__(self, other):
        return Empty

    def __div__(self, other):
        return Empty

    def __rdiv__(self, other):
        return Empty

    def __truediv__(self, other):
        return Empty

    def __rtruediv__(self, other):
        return Empty

    def __mod__(self, other):
        return Empty

    def __rmod__(self, other):
        return Empty

    def __divmod__(self, other):
        return Empty

    def __rdivmod__(self, other):
        return Empty

    def __pow__(self):
        return Empty

    def __rpow__(self):
        return Empty

    def __lshift__(self, other):
        return Empty

    def __rlshift__(self, other):
        return Empty

    def __rshift__(self, other):
        return Empty

    def __rrshift__(self, other):
        return Empty

    def __and__(self, other):
        return Empty

    def __rand__(self, other):
        return Empty

    def __or__(self, other):
        return Empty

    def __ror__(self, other):
        return Empty

    def __xor__(self, other):
        return Empty

    def __rxor__(self, other):
        return Empty

    def __hash__(self):
        return object.__hash__(self)

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration()


Empty = _Empty()


class EmptyDict(collections.defaultdict):
    def __init__(self, *args, **kwargs):
        """A defaultdict who's default values are an Empty and that can be
        accessed via attributes as well as normal dict methods.

        Useful for wrapping around nested dicts who's keys you can't be sure of
        and when you don't want to have to code too defensively.
        """
        super(EmptyDict, self).__init__(lambda x: Empty, *args, **kwargs)

    def __getattribute__(self, name):
        if hasattr(collections.defaultdict, name):
            return collections.defaultdict.__getattribute__(self, name)
        if collections.defaultdict.__contains__(self, name):
            data = collections.defaultdict.__getitem__(self, name)
            if isinstance(data, dict):
                return EmptyDict(**data)
            elif data is None:
                return Empty
            else:
                return data
        return Empty

    def __getitem__(self, item):
        if collections.defaultdict.__contains__(self, item):
            data = collections.defaultdict.__getitem__(self, item)
            if isinstance(data, dict):
                return EmptyDict(**data)
            elif data is None:
                return Empty
            else:
                return data
        return Empty

    def __missing__(self, key):
        return Empty

    def __repr__(self):
        return dict.__repr__(self)


def if_empty(value, return_if_empty=None):
    """Returns the value of the `return_if_empty` parameter (`None` by default)
    if the given `value` parameter is either an `Empty`.

    The point of this is to quickly default some value that may be an Empty OR
    some other value that evaluates as False into the correct type (e.g. before
    passing a possible `Empty` on to code that may bug out with an `Empty` but
    expect something like a `None` or a 0 or an empty string) without bothering
    with more cumbersome type checks.

    This can usually be done with a simple `or` fallback like so:

        >>> bar = Empty
        >>> foo = bar or None
        >>> assert foo is None  # GOOD: We wanted a None by default

    This ensures that if `bar` is an `Empty`, `foo` will be a
    `None` by default, however, if the expected real value of `bar` can be
    something that evaluates to `False` in an `or` check (eg. `None`, `False`,
    `0`, `0.0`, `""`, etc. this check will also always overwrite such real
    values with a `None`:

        >>> bar = 0
        >>> foo = if_empty(bar, None)
        >>> assert foo is None  # GOOD

    So we can guard agains this while skipping overly complex checks (that would
    negated the utility of the `Empty` stuff) like so:

        >>> bar = Empty
        >>> foo = if_empty(bar, None)
        >>> assert foo is None  # GOOD: Default None if no value is set
        >>> bar = 0
        >>> foo = if_empty(bar, None)
        >>> assert foo == 0  # GOOD: Value of 0 is cool

    :param value: Value to check if is an `Empty`
    :type value: Any
    :param return_if_empty: Value to return (as default) if the `value` is empty
    :type return_if_empty: Any
    :return: The `return_if_empty` param if `value` is an `Empty`, otherwise,
             the `value` unchanged
    :rtype: Any
    """
    if value is Empty:
        return return_if_empty
    return value
