__all__ = [
    'get_any',
    'get_module',
    'get_class',
    'get_callable',
    'get_methfunc',
    'get_function',
]

"""String Importing Utilities.

That is, functions to import and return python stuff via string during runtime.
"""
import importlib
import inspect
from ccptools.tpu import insp

import logging
log = logging.getLogger(__name__)


def get_any(string, default=None, logger=False, reraise=False):
    """Attempts to import and return anything via the given string.

    Anything here essentially means, module or any module attribute (stuff
    declared at the top level of a module like classes and functions).

    If the given string is not a string, the given parameter is simply
    returned back.

    This function is "silent" be default, i.e. it returns the given default (or
    None) if it fails to find the stuff to import without raising an exception.

    Set the reraise parameter to True in order to have this function raise any
    Exceptions it encounters.

    The logger parameter is False by default which means nothing is logged on
    any error but you can set it to True or None in order to log any Exceptions
    (e.g. ImportError or AttributeError) encountered.

    You can also set the logger parameter to any other logging.Logger in order
    to log to that logger instead of the module default (tpu.strimp).

    :param string: A string with the module or module attribute to try and
                   import.
    :type string: str, unicode or any
    :param default: The default value to return on failure.
    :type default: any
    :param logger: The logger to log errors to (False = No logging,
                   True/None = module default: ccptools.tpu.strimp)
    :type logger: bool or None or logging.Logger
    :param reraise: Should exceptions and errors encountered be reraised?
    :type reraise: bool
    :return: The module or whatever the given string was referring to or the
             default value given on failure.
    :rtype: any
    """
    if not isinstance(string, str):
        return string
    try:
        if '.' in string:
            ridx = string.rindex('.')
            mod_name = string[:ridx]
            any_name = string[ridx + 1:]
            from_module = importlib.import_module(mod_name)
            if hasattr(from_module, any_name):
                return getattr(from_module, any_name)
            else:  # Might be a module...?
                return importlib.import_module(string)
        else:  # Must be a module then...?
            return importlib.import_module(string)
    except ImportError as ex:
        if logger is not False:
            if logger is True or logger is None:
                logger = log
            logger.exception(u'ImportError in ccptools.tpu.strimp.get_any("%s"): %r', string, ex)
        if reraise:
            raise
    except AttributeError as ex:
        if logger is not False:
            if logger is True or logger is None:
                logger = log
            logger.exception(u'AttributeError in ccptools.tpu.strimp.get_any("%s"): %r', string, ex)
        if reraise:
            raise
    except Exception as ex:
        if logger is not False:
            if logger is True or logger is None:
                logger = log
            logger.exception(u'Exception in ccptools.tpu.strimp.get_any("%s"): %r', string, ex)
        if reraise:
            raise

    return default


def get_module(string, default=None, logger=False, reraise=False):
    """Attempts to import and return a python module via the given string.

    This is essentially just a call to get_any with the added check to see if
    the imported thing is a module, so see the get_any documentation for details.

    :param string: A string with the module to try and import.
    :type string: str, unicode or any
    :param default: The default value to return on failure.
    :type default: any
    :param logger: The logger to log errors to (False = No logging,
                   True/None = module default: tpu.strimp)
    :type logger: bool or None or logging.Logger
    :param reraise: Should exceptions and errors encountered be reraised?
    :type reraise: bool
    :return: The module or whatever the given string was referring to or the
             default value given on failure.
    :rtype: module or None
    """
    try:
        something = importlib.import_module(string)

        if inspect.ismodule(something):
            return something
        else:
            raise ValueError(u'Not a module: %s (it is "%s")' % (string, type(something)))
    except ValueError as ex:
        if logger is not False:
            if logger is True or logger is None:
                logger = log
            logger.exception(u'Exception in ccptools.tpu.strimp.get_module("%s"): %r', string, ex)
        if reraise:
            raise
    except Exception:
        if reraise:
            raise
    return default


def get_class(string, default=None, logger=False, reraise=False):
    """Attempts to import and return a class via the given string.

    This is essentially just a call to get_any with the added check to see if
    the imported thing is a class, so see the get_any documentation for details.

    :param string: A string with the class to try and import.
    :type string: str, unicode or any
    :param default: The default value to return on failure.
    :type default: any
    :param logger: The logger to log errors to (False = No logging,
                   True/None = module default: tpu.strimp)
    :type logger: bool or None or logging.Logger
    :param reraise: Should exceptions and errors encountered be reraised?
    :type reraise: bool
    :return: The module or whatever the given string was referring to or the
             default value given on failure.
    :rtype: class or type or None
    """
    try:
        something = get_any(string, None, logger=logger, reraise=True)
        if inspect.isclass(something):
            return something
        else:
            raise ValueError(u'Not a class: %s (it is "%s")' % (string, type(something)))
    except ValueError as ex:
        if logger is not False:
            if logger is True or logger is None:
                logger = log
            logger.exception(u'Exception in ccptools.tpu.strimp.get_class("%s"): %r', string, ex)
        if reraise:
            raise
    except Exception:
        if reraise:
            raise
    return default


def get_callable(string, default=None, logger=False, reraise=False):
    """Attempts to import and return a callable via the given string.

    This is essentially just a call to get_any with the added check to see if
    the imported thing is a callable via tpu.insp.is_callable.

    :param string: A string with the callable to try and import.
    :type string: str, unicode or any
    :param default: The default value to return on failure.
    :type default: any
    :param logger: The logger to log errors to (False = No logging,
                   True/None = module default: tpu.strimp)
    :type logger: bool or None or logging.Logger
    :param reraise: Should exceptions and errors encountered be reraised?
    :type reraise: bool
    :return: The module or whatever the given string was referring to or the
             default value given on failure.
    :rtype: function or method or object or None
    """
    try:
        something = get_any(string, None, logger=logger, reraise=True)
        if insp.is_callable(something):
            return something
        else:
            raise ValueError(u'Not callable: %s (it is "%s")' % (string, type(something)))
    except ValueError as ex:
        if logger is not False:
            if logger is True or logger is None:
                logger = log
            logger.exception(u'Exception in ccptools.tpu.strimp.get_callable("%s"): %r', string, ex)
        if reraise:
            raise
    except Exception:
        if reraise:
            raise
    return default


def get_methfunc(string, default=None, logger=False, reraise=False):
    """Attempts to import and return a callable via the given string.

    This is essentially just a call to get_any with the added check to see if
    the imported thing is a method or function via tpu.insp.is_methfunc.

    :param string: A string with the method or function to try and import.
    :type string: str, unicode or any
    :param default: The default value to return on failure.
    :type default: any
    :param logger: The logger to log errors to (False = No logging,
                   True/None = module default: tpu.strimp)
    :type logger: bool or None or logging.Logger
    :param reraise: Should exceptions and errors encountered be reraised?
    :type reraise: bool
    :return: The module or whatever the given string was referring to or the
             default value given on failure.
    :rtype: function or method or None
    """
    try:
        something = get_any(string, None, logger=logger, reraise=True)
        if insp.is_methfunc(something):
            return something
        else:
            raise ValueError(u'Not a method or function: %s (it is "%s")' % (string, type(something)))
    except ValueError as ex:
        if logger is not False:
            if logger is True or logger is None:
                logger = log
            logger.exception(u'Exception in ccptools.tpu.strimp.get_methfunc("%s"): %r', string, ex)
        if reraise:
            raise
    except Exception:
        if reraise:
            raise
    return default


def get_function(string, default=None, logger=False, reraise=False):
    """Attempts to import and return a callable via the given string.

    This is essentially just a call to get_any with the added check to see if
    the imported thing is a method or function via tpu.insp.is_methfunc.

    :param string: A string with the function to try and import.
    :type string: str, unicode or any
    :param default: The default value to return on failure.
    :type default: any
    :param logger: The logger to log errors to (False = No logging,
                   True/None = module default: tpu.strimp)
    :type logger: bool or None or logging.Logger
    :param reraise: Should exceptions and errors encountered be reraised?
    :type reraise: bool
    :return: The module or whatever the given string was referring to or the
             default value given on failure.
    :rtype: function or method or None
    """
    try:
        something = get_any(string, None, logger=logger, reraise=True)
        if inspect.isfunction(something):
            return something
        else:
            raise ValueError(u'Not a function: %s (it is "%s")' % (string, type(something)))
    except ValueError as ex:
        if logger is not False:
            if logger is True or logger is None:
                logger = log
            logger.exception(u'Exception in ccptools.tpu.strimp.get_function("%s"): %r', string, ex)
        if reraise:
            raise
    except Exception:
        if reraise:
            raise
    return default
