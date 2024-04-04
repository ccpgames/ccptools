__all__ = [
    'any_getter',
    'any_setter',
    'nested_get',
    'nested_set',
]
from ccptools.tpu.structs import *


def any_getter(obj: Any, key: Union[str, int], default: Any = None, eval_call: bool = False) -> Optional[Any]:
    if isinstance(key, int):
        try:
            val = obj[key]
        except (IndexError, KeyError):
            return default
    else:
        if isinstance(obj, Mapping):
            val = obj.get(key, default)
        else:
            val = getattr(obj, key, default)
    if eval_call:
        if val and isinstance(val, Callable):
            val = val()
    return val


def any_setter(obj: Any, key: Union[str, int], value: Any):
    if isinstance(obj, MutableSequence):
        obj[key] = value

    elif isinstance(obj, MutableMapping):
        obj[key] = value

    elif isinstance(key, int):
        obj[key] = value

    else:
        setattr(obj, key, value)


def nested_get(obj: Union[Mapping, Sequence],
               key_list: Sequence[Union[str, int]],
               default: Any = None) -> Any:
    """Given a nested Mapping, Sequence or any indexable/subscriptable object of
    other such, and a Sequence of keys and/or indexes, fetches the object at the
    end of the Sequence of keys.

    Returns the given default value if any key/index isn't found (defaults to
    None if nothing is given).

    Example:
    >>> nested_get({'a': {7: {'c': ['apple', 'banana', 'cantaloupe']}, 5: 'other'}}, ('a', 7, 'c', -2))
    'banana'
    """
    next_obj = obj
    for key in key_list:
        next_obj = any_getter(next_obj, key, None)
        if next_obj is None:
            return default
    return next_obj


def nested_set(obj: Union[Mapping, Sequence],
               key_list: Sequence[Union[str, int]],
               value: Any):
    """Given a nested Mapping, Sequence or any indexable/subscriptable object of
    other such, and a Sequence of keys and/or indexes, sets the value the those
    keys/indexes point to.

    If any key/index doesn't exist, it will be created/set if possible

    """
    next_obj = obj
    last = key_list[-1]
    path = key_list[:-1]
    for key in path:
        next_next_obj = any_getter(next_obj, key, None)
        if next_next_obj is None:
            next_next_obj = {}
            any_setter(next_obj, key, next_next_obj)
        next_obj = next_next_obj

    any_setter(next_obj, last, value)

