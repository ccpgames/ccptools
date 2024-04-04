__all__ = [
    'group_by',
]

from ccptools.tpu.structs import *

T_OBJ = TypeVar('T_OBJ')


def group_by(list_of_stuff: Iterable[T_OBJ],
             key_getter: Union[str, int, Callable]) -> Dict[Any, List[T_OBJ]]:
    """Given a list of stuff and a "key getter", returns a dict with key value
    pairs of the values given by the "key getter" as the unique keys in that
    dict and the values a list of the stuffs from the given list who's "key
    getter" values matched the return dicts key.

    In other words, groups a list of things by the values returned by the "key
    getter" to a dict.

    The "key getter" can be any of the following, resulting in slightly different
    functionality based on type:
     - A str: will try and fetch an attribute with that name from each object in
     the list of stuff or use the string as a key if the object is a dict like.
     If that attribute is a method or other callable, it will be called with the
     expectation that it's the name of an accessor method that will return the
     relevant key value.
     - An int: will assume this is an index so it will be used in a indexing
     getitem call.
     - Any callable: will assume a method that takes in an object of the type in
     the list of stuff and returns the required value from the object to use as
     a key and group the objects by.
    """
    group_map: Dict[Hashable, List[T_OBJ]] = {}
    if isinstance(key_getter, (str, int)):
        from ccptools.tpu.iters import any_getter
        getter_call = lambda x: any_getter(x, key_getter)

    else:
        getter_call = key_getter

    for stuff in list_of_stuff:
        a = getter_call(stuff)
        if isinstance(a, Callable):
            a = a()

        if a not in group_map:
            group_map[a] = []
        group_map[a].append(stuff)

    return group_map
