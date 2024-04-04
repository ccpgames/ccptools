__all__ = [
    'UniversalSerializer',
]

from ccptools.tpu.structs._base import *


class UniversalSerializer(object):
    _emptyables = (list, tuple, set, dict, str, bytes)

    def __init__(self, skip_keys=None, skip_values=None, skip_private=True, skip_nones=False, skip_empties=False,
                 max_depth=0):
        """Serializes any python object or type recursively.

        What this means in practical terms is that anything this function is given
        will be guaranteed to be of and/or only contain the following python types:
            - int
            - float
            - str
            - bytes
            - decimal.Decimal
            - datetime.date
            - datetime.datetime
            - datetime.time
            - datetime.timedelta
            - None
            - list
            - tuple
            - set
            - dict

        The main purpose/use-case for this is to take any arbitrary classes and/or
        data structures (e.g. from various third party APIs) and turn them into
        simple/common python primary types for safer manipulation and/or use.

        This minimizes the amount of "defensive" coding needed to handle external
        return values who's structures are wholly or partially unknown or might
        change without notice. Turning an object into a discrete set of types means
        that checking for attributes and values becomes easier and less likely to
        raise annoying exceptions that need handling like AttributeError,
        ValueError, KeyError and such.

        An example would be turning an object into a dict to ensure that calling
        obj.get('is_foo', False) simply yields True or False without any additional
        safety measures or exception handling and such.

        Another example would be to turn an object into a dict guaranteed to have
        all it's properties and recursive structures for dumping out in logs or
        encoding into other formats like JSON (although you'd have to handle the
        serialization of values from the datetime and decimal modules specially for
        that).

        These python types are returned as-is:
            - int
            - float
            - str
            - bytes
            - decimal.Decimal
            - datetime.date
            - datetime.datetime
            - datetime.time
            - datetime.timedelta
            - None

        These types are returned back (as either lists or dicts) after recursively
        serializing their values and/or properties:
            - list
            - tuple
            - set
            - dict

        Any other type (e.g. anything inheriting from object) that has a __dict__
        property will be serialized recursively to a dict by using their __dict__.

        Other types without a __dict__ property will yield the string:
            - '__WHAT__::%s' % type(obj)

        Reference loops will be serialized as the string
            - '__LOOP__::%s::%s' % (type(obj), id(obj))


        :param skip_keys: List of key names to skip from dict and object.__dict__
                          serialization
        :type skip_keys: list | tuple | set
        :param skip_values: List of values to skip from dict and object.__dict__
                            serialization
        :type skip_values: list | tuple | set
        :param skip_private: Should private keys (i.e. who's name starts with an
                             underscore) be skipped? Default is True.
        :type skip_private: bool
        :param skip_nones: Should values of None be skipped from dict and
                           object.__dict__ serialization? Default is False.
        :type skip_nones: bool
        :param skip_empties: Should empty lists, tuples, sets, dicts, strings and
                             bytes be skipped from dict and object.__dict__
                             serialization? Default is False.
        :type skip_empties: bool
        :param max_depth: Maximum recursion depth (Default is 0 for infinite)
        :type max_depth: int

        """
        self.skip_keys = list(skip_keys or [])
        self.skip_values = list(skip_values or [])

        self.skip_private = skip_private
        self.skip_nones = skip_nones
        self.skip_empties = skip_empties
        self.max_depth = max_depth

        self._breadcrumbs = []

        self.serialize_map = {
            int: self._serialize_int,
            float: self._serialize_float,
            str: self._serialize_str,
            bytes: self._serialize_bytes,

            decimal.Decimal: self._serialize_decimal,

            datetime.time: self._serialize_time,
            datetime.date: self._serialize_date,
            datetime.datetime: self._serialize_datetime,
            datetime.timedelta: self._serialize_timedelta,

            list: self._serialize_list,
            tuple: self._serialize_tuple,
            set: self._serialize_set,
            dict: self._serialize_dict,
        }

    def serialize(self, obj):
        self._breadcrumbs = []  # Just in case!
        return self._serialize_any(obj)

    def _serialize_any(self, obj):
        try:
            if obj in self._breadcrumbs:
                return self._serialize_loop(obj)

            if obj is None:
                return self._serialize_none(obj)

            if self.max_depth and len(self._breadcrumbs) > self.max_depth:
                return self._serialize_max_depth(obj)

            t = type(obj)
            serializer = self.serialize_map.get(t, self._serialize_other)
            if serializer:
                self._breadcrumbs.append(obj)
                value = serializer(obj)
                self._breadcrumbs.pop()
                return value

        except Exception as ex:
            return self._serialize_error(obj, '%s' % ex)

        return None

    def _serialize_int(self, obj):
        """
        :type obj: int
        :rtype: int
        """
        return obj

    def _serialize_float(self, obj):
        """
        :type obj: float
        :rtype: float
        """
        return obj

    def _serialize_str(self, obj):
        """
        :type obj: str
        :rtype: str
        """
        return obj

    def _serialize_bytes(self, obj):
        """
        :type obj: bytes
        :rtype: bytes
        """
        return obj

    def _serialize_decimal(self, obj):
        """
        :type obj: decimal.Decimal
        :rtype: decimal.Decimal
        """
        return obj

    def _serialize_datetime(self, obj):
        """
        :type obj: datetime.datetime
        :rtype: datetime.datetime
        """
        return obj

    def _serialize_time(self, obj):
        """
        :type obj: datetime.time
        :rtype: datetime.time
        """
        return obj

    def _serialize_date(self, obj):
        """
        :type obj: datetime.date
        :rtype: datetime.date
        """
        return obj

    def _serialize_timedelta(self, obj):
        """
        :type obj: datetime.timedelta
        :rtype: datetime.timedelta
        """
        return obj

    def _serialize_list(self, obj):
        """
        :type obj: list
        :rtype: list
        """
        return self._serialize_iters(obj)

    def _serialize_tuple(self, obj):
        """
        :type obj: tuple
        :rtype: list
        """
        return self._serialize_iters(obj)

    def _serialize_set(self, obj):
        """
        :type obj: set
        :rtype: list
        """
        return self._serialize_iters(obj)

    def _serialize_iters(self, obj):
        """
        :type obj: list | tuple | set
        :rtype: list
        """
        return [self._serialize_any(i) for i in obj]

    def _serialize_maps(self, obj):
        """
        :type obj: dict
        :rtype: dict
        """
        d = {}
        for k, v in obj.items():
            if k in self.skip_keys or v in self.skip_values:
                continue
            if self.skip_private and isinstance(k, str) and k.startswith('_'):
                continue
            if self.skip_nones and v is None:
                continue
            val = self._serialize_any(v)
            if self.skip_empties and isinstance(val, self._emptyables) and not val:
                continue
            d[k] = val
        return d

    def _serialize_dict(self, obj):
        """
        :type obj: dict
        :rtype: dict
        """
        return self._serialize_maps(obj)

    def _serialize_object(self, obj):
        """
        :type obj: object
        :rtype: dict
        """
        return self._serialize_maps(obj.__dict__)

    def _serialize_other(self, obj):

        # OVERRIDE CUSTOM SERIALIZING HERE!

        # If no special serializers are found, just serialize the __dict__ of an object!
        if hasattr(obj, '__dict__'):
            return self._serialize_object(obj)
        return self._serialize_derived(obj)

    def _serialize_none(self, obj):
        """
        :type obj: None
        :rtype: None
        """
        return None

    def _serialize_loop(self, obj):
        return '__LOOP__::%s::%s' % (type(obj), id(obj))

    def _serialize_derived(self, obj):
        for t, func in self.serialize_map.items():
            # Check if the object extends any of our known types and use that
            if isinstance(obj, t):
                return func(obj)

        # If all else fails, return unknown serialization
        return self._serialize_unknown(obj)

    def _serialize_error(self, obj, error):
        return '__ERROR__::%s::%s' % (type(obj), error)

    def _serialize_unknown(self, obj):
        return '__UNKNOWN__::%s' % type(obj)

    def _serialize_max_depth(self, obj):
        return '__MAX_DEPTH__::%s::%s' % (type(obj), id(obj))
