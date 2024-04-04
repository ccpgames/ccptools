__all__ = [
    'AttributeFluidObject',
]

import logging
_default_log = logging.getLogger(__name__)


class AttributeFluidObject(object):
    _log_missing_attributes = False
    _log_level = logging.WARNING
    _logger = _default_log
    _default_value = None

    def __new__(cls, *args, **kwargs):
        # This makes sure we don't log anything set in the __init__ methods
        # as missing until AFTER calling AttributeFluidObject's super init.
        instance = super(AttributeFluidObject, cls).__new__(cls)

        object.__setattr__(instance, '_log_missing_attributes', False)
        return instance

    def __init__(self, **kwargs):
        """Base class for "Attribute-Fluid" object, i.e. objects that
        self-correct instead of raising an attribute error when an attribute
        called is missing (whether it's set or get), i.e. create within itself
        any missing attribute on the fly.

        Useful for making error tolerant objects, e.g. when external resources
        (that aren't guaranteed to be stable) are used to act on the object. A
        good example would be a Class that read configuration values from a
        file where you don't want the code to break even if the file has borked
        values.

        The class has three class variables that determine how to handle
        missing attributes specifically:

            - _log_missing_attributes: If True, the object will log any missing
              attribute call (for the first time). This will be logged to the
              tpu.bases logger. Default is False.
            - _logger: The logger to log to (if _log_missing_attributes is
              True). Default is the 'tpu.bases'.
            - _log_level: The log level to log missing attributes as (if
              _log_missing_attributes is True). Default is logging.WARNING.
            - _default_value: The default value to give to missing attributes
              created. Default is None.

        IMPORTANT: If logging missing attributes, make sure you call:
        `super(self.__class__, self).__init__(**kwargs)` in your classes
        `__init__` method AFTER setting all expected attributes (generally at
        the bottom of the __init__ method). Otherwise missing attributes will
        not get logged AND is you call the super's __init__ before initializing
        all self.whatever attributes, those attributes in the init that you set
        after calling the super will get logged as missing, which is both
        incorrect and annoying :).

        :param kwargs: Any keywords that will be set as attributes of the
                       object.
        :type kwargs: dict[any,any]
        """
        object.__setattr__(self, '_log_missing_attributes', self.__class__._log_missing_attributes)
        if kwargs:
            for k, v in kwargs.items():
                if not k.startswith('_'):
                    setattr(self, k, v)

    def __getattr__(self, item):
        if self._log_missing_attributes:
            self._logger.log(self._log_level, u'Attribute "%s" of Class "%s" does not exist! Setting it to default value=%r', item, self.__class__.__name__, self._default_value)
        object.__setattr__(self, item, self._default_value)
        return self._default_value

    def __setattr__(self, name, value):
        if self._log_missing_attributes:
            if not hasattr(self, name):
                self._logger.log(self._log_level, u'Attribute "%s" of Class "%s" does not exist but is now set to %r!', name, self.__class__.__name__, value)
        object.__setattr__(self, name, value)
