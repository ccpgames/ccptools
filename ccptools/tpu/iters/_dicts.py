__all__ = [
    'nested_dict_update',
    'nest_dict',
    'str_nest_dict',
    'flatten_dict',
    'str_flatten_dict',
]

from ccptools.tpu.structs import *


def nested_dict_update(base_map: Dict[Any, Any], update_map: Dict[Any, Any]):
    """Updates a nested dicts. This means that if the `base_map` and
    `update_map` contain the same key that is a dict in both, that nested dict
    will be updated the same way `base_map.update(update_map)` works, i.e. it
    will preserve any pre-existing keys in `base_map` and only update the values
    of keys in the `update_map` (again, in a nested way).

    Example of normal update:
    >>> a = {'foo': 1, 'bar': {'alpha': 2, 'beta': 3}, 'oof': 4}
    >>> b = {'foo': 101, 'bar': {'beta': 103}}
    >>> a.update(b)
    >>> print(a)
    {'foo': 101, 'bar': {'beta': 103}, 'oof': 4}

    Example of nested update:
    >>> a = {'foo': 1, 'bar': {'alpha': 2, 'beta': 3}, 'oof': 4}
    >>> b = {'foo': 101, 'bar': {'beta': 103}}
    >>> nested_dict_update(a, b)
    >>> print(a)
    {'foo': 101, 'bar': {'alpha': 2, 'beta': 103}, 'oof': 4}

    Note that if a key (or nested key) who's value is a dict in `base_map` is
    NOT a dict in `update_map`, that dict value will be overwritten completely
    with the new value and type.
    """
    for k, v in update_map.items():
        if k in base_map:
            base_val = base_map[k]
            if isinstance(base_val, dict) and isinstance(v, dict):
                nested_dict_update(base_val, v)
                base_map[k] = base_val
            else:
                base_map[k] = v
        else:
            base_map[k] = v


def nest_dict(key_list: List[Any], value: Any = None) -> Dict[Any, Any]:
    """Creates a nested dict using a list of keys to construct an ever deepening
    dict of a dict of a dict etc.

    Example:
    >>> nest_dict(['a', 'b', 'c'], 'value')
    {'a': {'b': {'c': 'value'}}}
    """
    if not key_list:
        return value
    k = key_list.pop(0)
    return {k: nest_dict(key_list, value)}


def str_nest_dict(nested_key_string: str, value: Any = None, key_seperator: str = '.') -> Dict[str, Any]:
    """Creates a nested dict using a string with some separator symbol to split
    it into a list of keys to construct an ever deepening dict of a dict of a
    dict etc.

    Example:
    >>> str_nest_dict('a.b.c', 'value')
    {'a': {'b': {'c': 'value'}}}
    """
    return nest_dict(nested_key_string.split(key_seperator), value)


def _denest_dict(some_dict: Dict[Any, Any]) -> List[Tuple[List[Any], Any]]:
    """Takes a potentially nested dict and returns a list of Tuple pairs
    containing all "leaf" values (values that aren't dicts) as each Tuples
    second value while the first value will be a list of the "key-path" through
    the nested dict to that value.

    Example:
    >>> _denest_dict({'a': {7: {'c': 'value'}, 5: 'other'}})
    [(['a', 7, 'c'], 'value'), (['a', 5], 'other')]
    """
    buff = []
    for k, v in some_dict.items():
        if isinstance(v, dict):
            for nk, nv in _denest_dict(v):
                buff.append(([k]+nk, nv))
        else:
            buff.append(([k], v))
    return buff


def flatten_dict(some_dict: Dict[Any, Any]) -> Dict[Tuple, Any]:
    """Takes a dict that may (or may not) be nested (contain other dicts) and
    flattens it out by keys, returning a single dict with one value entry per
    "leaf" value (any value in the nested dict tree that is NOT another dict)
    where they key for each value is a tuple of the key "path" to it in the
    original dict.

    >>> flatten_dict({'a': {7: {'c': 'value'}, 5: 'other'}})
    {('a', 7, 'c'): 'value', ('a', 5): 'other'}
    """
    buff = {}
    for k, v in _denest_dict(some_dict):
        buff[tuple(k)] = v
    return buff


def str_flatten_dict(some_dict: Dict[str, Any], joiner: str = '.', caster: Callable = str) -> Dict[str, Any]:
    """Does the same as `flatten_dict` except instead of keys of tuples, keys
    are converted to str and joined with a dot character (by default).

    Both the joining character (or string) and how each value in the key tuple
    is converted to a str is customizable.

    This can be especially useful if keys contain objects who's hash values
    differ but who's str representations are the same, e.g. the int 1 and the
    string '1' in {1: 'a', '1': 'b'}. That dict will turn into {'1': 'b'}.

    :type some_dict: dict
    :type joiner: str
    :type caster: function
    :rtype: dict[str,Any]
    """
    buff = {}
    for k, v in _denest_dict(some_dict):
        buff[joiner.join([caster(ki) for ki in k])] = v
    return buff
