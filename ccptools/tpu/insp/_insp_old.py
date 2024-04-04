__all__ = [
    'is_methfunc',
    'is_callable',
    'get_argspec',
    'fits_callable_profile',
    'get_any_name',
    'get_first_attr',
    'resolve_attr',
    'resolve_first',
]

from ccptools.tpu.structs import empty
import inspect
from typing import *

_NOT_SUPPLIED = object()


def is_methfunc(function_or_method):
    """Checks if the given parameter is a function/method or not.

    This simply joins python's inspect.isfunction and inspect.ismethod in one
    call.

    A function is:
        - Anything declared via def on the top level of a module (or inside
          another function or method)
        - Anything created with lambda
        - Any method defined in a class with the @staticmethod decorator
    A method is:
        - Anything declared via def inside a class definition (except those
          that have the @staticmethod decorator)

    :param function_or_method: The thing to check
    :type function_or_method: function or method or any
    :return: True if the given parameter is a function or a method, false if not
    :rtype: bool
    """
    return inspect.isfunction(function_or_method) or inspect.ismethod(function_or_method)


def is_callable(something):
    """Checks if the given parameter is callable or not.

    Callable means a function, method or object of a class that implements the
    __call__ method and can therefor be called like a function.

    See is_methfunc() for more details.

    :param something: The thing to check
    :type something: function or method or object or any
    :return: True if the given parameter is callable, false if not
    :rtype: bool
    """
    if is_methfunc(something):
        return True
    else:
        call_func = getattr(something, '__call__', None)
        if call_func:
            return is_methfunc(call_func)
    return False


def get_argspec(somecallable):
    """Gets the argument specifications of a callable.

    This simply extends the inspect.getargspec function to also work for
    objects of classes that implement the __call__ method.

    Returns None if the given parameter isn't callable.

    :param somecallable: The thing to fetch the argument spec for
    :type somecallable: function or method or object or any
    :return: The argspecs or None if the given parameter wasn't callable
    :rtype: inspect.ArgSpec or collections.namedtuple or None
    """
    if is_methfunc(somecallable):
        return inspect.getfullargspec(somecallable)
    else:
        call_func = getattr(somecallable, '__call__', None)
        if call_func:
            if is_methfunc(call_func):
                return inspect.getfullargspec(call_func)
    return None


def fits_callable_profile(somecallable, required_arg_count=None,
                          total_arg_count=None, default_count=None,
                          has_varargs=None, has_kwargs=None, arg_names=None,
                          raise_error=False):
    """Checks if a callable (function, method or object with __call__) fits
    the given argument profile.

    Returns False if the given parameter to check is not callable.

    All check parameters default to None which skips that particular check.

    Required arguments means total number of arguments minus the number of
    arguments with default values.

    If the arg_names parameter is a list (NOT a tuple), this will only check
    if the argument names there in are present regardless of order.

    If the arg_names parameter is a tuple (NOT a list), this will check if the
    order pf the argument names there in are present and in the same order
    although you can use '*' in the tuple to skip the check for the argument
    in that place (e.g. if you don't care what the "self" parameter in a bound
    method is called but you need a certain argument set to be present in order
    after that). The arg_names tuple can be shorter than the number of
    arguments in the callable though without that failing (use the argument
    count checks if that is needed).

    :param somecallable: The thing to check
    :type somecallable: function or method or object or any
    :param required_arg_count: The number of required arguments (if given),
                               either the exact number or a 2-tuple with
                               the minimum and maximum allowed number.
    :type required_arg_count: int or (int, int) or None
    :param total_arg_count: The total number of arguments (if given), either
                            the exact number or a 2-tuple with the minimum
                            and maximum allowed number.
    :type total_arg_count: int or (int, int) or None
    :param default_count: The number of arguments with default values (if
                          given), either the exact number or a 2-tuple with
                          the minimum and maximum allowed number.
    :type default_count: int or (int, int) or None
    :param has_varargs: Should the callable accept a variable number of
                        arguments (*args)? If this is a string, then
                       the args argument must be called that to pass.
    :type has_varargs: bool or str or None
    :param has_kwargs: Should the callable accept a variable number of
                       named arguments (**kwargs)? If this is a string, then
                       the kwargs argument must be called that to pass.
    :type has_kwargs: bool or str or None
    :param arg_names: A list of argument names the callable should have or a
                      tuple of argument names the callable should have in that
                      exact order (using "*" to skip individual name checks).
    :type arg_names: list[str] or tuple[str] or None
    :param raise_error: Should an ValueError be raised if a check fails
                        (with the details)?
    :type raise_error: bool
    :return: True if the given callable fits all the given profile checks,
             False if not.
    :rtype: bool
    """
    # TODO(thordurm@ccpgames.com) 2024-03-20: This could probably use a "modern"
    #  overhaul and to include type annotations and such!... I think this was
    #  written for Python 2.7 :D
    specs = get_argspec(somecallable)
    if not specs:
        if raise_error:
            raise ValueError('Not a callable!')
        return False
    def_count = 0
    if specs.defaults:
        def_count = len(specs.defaults)
    arg_count = 0
    if specs.args:
        arg_count = len(specs.args)
    req_args = arg_count - def_count

    if required_arg_count is not None:
        if isinstance(required_arg_count, (list, tuple)):
            mi = required_arg_count[0]
            ma = required_arg_count[1]
        else:
            mi = required_arg_count
            ma = required_arg_count
        if not mi <= req_args <= ma:
            if raise_error:
                raise ValueError('Required arguments check fail: min=%s >= count=%s >= max=%s' % (mi, req_args, ma))
            return False  # Required argument count fail! :(

    if total_arg_count is not None:
        if isinstance(total_arg_count, (list, tuple)):
            mi = total_arg_count[0]
            ma = total_arg_count[1]
        else:
            mi = total_arg_count
            ma = total_arg_count
        if not mi <= arg_count <= ma:
            if raise_error:
                raise ValueError('Arguments count check fail: min=%s >= count=%s >= max=%s' % (mi, arg_count, ma))
            return False  # Total argument count fail! :(

    if default_count is not None:
        if isinstance(default_count, (list, tuple)):
            mi = default_count[0]
            ma = default_count[1]
        else:
            mi = default_count
            ma = default_count
        if not mi <= def_count <= ma:
            if raise_error:
                raise ValueError('Default argument check fail: min=%s >= count=%s >= max=%s' % (mi, def_count, ma))
            return False  # Default argument count fail! :(

    if has_varargs is not None:
        if isinstance(has_varargs, str):
            if has_varargs != specs.varargs:
                if raise_error:
                    raise ValueError('Variable arguments name fail: is=%s, should be=%s' % (specs.varargs, has_varargs))
                return False  # Has variable arguments fail! :(
        if bool(has_varargs) != bool(specs.varargs):
            if raise_error:
                raise ValueError('Variable arguments fail: is=%s, should be=%s' % (bool(specs.varargs), bool(has_varargs)))
            return False  # Has variable arguments fail! :(

    if has_kwargs is not None:
        kwarg_name = specs.varkw
        if isinstance(has_kwargs, str):
            # if has_kwargs != specs.keywords:
            if has_kwargs != kwarg_name:
                if raise_error:
                    raise ValueError('Keyword arguments name fail: is=%s, should be=%s' % (kwarg_name, has_kwargs))
                return False  # Has variable keyword arguments fail! :(
        # if bool(has_kwargs) != bool(specs.keywords):
        if bool(has_kwargs) != bool(kwarg_name):
            if raise_error:
                raise ValueError('Keyword arguments fail: is=%s, should be=%s' % (bool(kwarg_name), bool(has_kwargs)))
            return False  # Has variable keyword arguments fail! :(

    if arg_names:
        if not specs.args:
            if raise_error:
                raise ValueError('Named arguments fail: No named arguments found')
            return False  # Has argument name fail! :(
        if isinstance(arg_names, list):  # Order doesn't matter!
            for arg_name in arg_names:
                if arg_name not in specs.args:
                    if raise_error:
                        raise ValueError('Named arguments fail: Argument "%s" not found' % arg_name)
                    return False  # Missing required argument! :(
        elif isinstance(arg_names, tuple):
            for i, arg_name in enumerate(arg_names):
                if specs.args[i] != arg_name and arg_name != '*':
                    if raise_error:
                        raise ValueError('Named arguments fail: Argument "%s" not found in correct order' % arg_name)
                    return False  # Missing required argument in order! :(
        else:
            if raise_error:
                raise ValueError('Named arguments fail: arg_names must be a list or tuple')
            return False

    return True  # Looks good! :D


def get_any_name(anything: Any) -> str:
    if anything is None:
        return 'None'

    if anything is empty.Empty:
        return f'{get_any_name(empty)}.Empty'

    if inspect.ismodule(anything):
        return getattr(anything, '__name__', f'?m:{anything!r}?')

    if isinstance(anything, property):
        anything = anything.fget

    if inspect.isfunction(anything) or inspect.ismethod(anything):
        module = getattr(anything, '__module__', None)
        if module and module != 'builtins':
            return f"{module}.{getattr(anything, '__qualname__', getattr(anything, '__name__', '?f1:noname?'))}"
        else:
            return f"{getattr(anything, '__qualname__', getattr(anything, '__name__', '?f1:noname?'))}"

    cls = None
    module = None
    if isinstance(anything, Type):  # noqa
        # Got a class/type/metaclass etc.
        cls = anything

    else:
        cls = getattr(anything, '__class__', None)

    if not cls:
        return f'?{anything!r}?'  # Worth a shot!

    name = getattr(cls, '__name__', None)
    if not name:
        name = f'??{cls!r}??'

    module = getattr(cls, '__module__', None)
    if module == 'builtins':
        module = ''

    if module is None:
        module = '?nomodule?'

    if module:
        return f'{module}.{name}'

    else:
        return f'{name}'


def get_first_attr(obj: Any, list_of_attributes: Union[str, List[str]], default: Any = None,
                   skip_nones: bool = False) -> Any:
    """Gets the first attribute of an object found from the given list of
    attribute names.

    This is similar to looping through a list using `getattr` although this will
    also work on dicts and dict like mapping objects.
    """
    from ccptools.tpu.iters import any_getter
    for attr_name in list_of_attributes:
        attr = any_getter(obj, attr_name, _NOT_SUPPLIED)
        if attr != _NOT_SUPPLIED:
            if skip_nones and attr is None:
                continue
            else:
                return attr

    return default


def resolve_attr(attr: Union[Callable, property, Any]) -> Any:
    """Resolves an attribute that may be a property or something callable to
    it's post-call value and returns.

    If the attr given is not a property or a callable entity, it's assumed to
    be a proper value to begin with and is returned unchanged.
    """
    if isinstance(attr, property):
        attr = attr.fget

    if callable(attr):
        return attr()

    return attr


def resolve_first(obj: Any, list_of_attributes: Union[str, List[str]], default: Any = None,
                  skip_nones: bool = False) -> Any:
    """Resolves the first attribute of an object found from the given list of
    attribute names that may be a property or something callable to it's
    post-call value and returns.

    Basically just a shortcut for using `get_first_attr` and `resolve_attr` at
    once.
    """
    attr = get_first_attr(obj, list_of_attributes, _NOT_SUPPLIED, skip_nones=skip_nones)
    if attr == _NOT_SUPPLIED:
        return default
    else:
        return resolve_attr(attr)
