__all__ = [
    'SentientObject',
]


class _SentientClassBuilder(type):
    """This is a sneaky Python black magic way to be able to collect certain
    methods of classes and add some meta data to the via decorated during the
    classes initialization.
    """
    def __new__(mcs, clsname, bases, dct):
        the_class = super(_SentientClassBuilder, mcs).__new__(mcs, clsname, bases, dct)
        my_map = {}
        for name, attr in dct.items():
            if hasattr(attr, '__call__'):
                sentience = getattr(attr, '__sentience__', None)
                if sentience is not None and isinstance(sentience, dict):
                    my_map[name] = sentience

        current_map = getattr(the_class, '__sentient_method_map__', None) or {}
        current_map[clsname] = my_map
        setattr(the_class, '__sentient_method_map__', current_map)
        return the_class


class SentientObject(object, metaclass=_SentientClassBuilder):
    """Having a class extend this instead of the normal python object allows
    you to mark some of it's methods via the sentient decorator and give them
    some meta-data. The names of those methods along with the metadata (using
    kwargs in the decorator) will be collected during the classes
    initialization (on first import) and added to the __sentient_method_map__
    dict. The sentient_methods() class method will return that map as such:
    {
        'method_name_1': {
            'meta_data_1': 'meta_value_1',
            'meta_data_2': 'meta_value_2'
        },
        'method_name_2': {
            'meta_data_1': 'meta_value_1',
            'meta_data_2': 'meta_value_2'
        }
    } ... etc.

    The point is simply to be able to flag certain methods in code with a
    simple decorator (as oppose to hardcoding some list) and then retrieve
    that list for whatever reason e.g. quickly and simply "exposing" (or
    advertising really) some methods to other code systematically (i.e.
    instant automatic API).


    """
    __sentient_method_map__ = {}

    @classmethod
    def sentient_methods(cls, inherited=True):
        """Returns the map of "sentient" methods and their meta data.

        :return: A dict with "sentient" method names as keys and a dict of
        their meta data as value.
        :rtype: dict
        """
        buff = cls.__sentient_method_map__[cls.__name__]
        if inherited:
            for basecls in cls.__bases__:
                if issubclass(basecls, SentientObject):
                    buff.update(basecls.sentient_methods())
        return buff

    @staticmethod
    def sentient(**kwargs):
        """Adds the given keywords to a new attribute of the decorated
        function, thus marking it for the SentientClassBuilder and storing
        the meta data.

        This triggers the SentientClassBuilder to add the method's name and
        meta data to the __sentient_method_map__ when the class (not object)
        is created.

        :param kwargs: The meta data to store
        :type kwargs: dict
        :return: The original function with the meta data added to it
        :rtype: function
        """
        def inner(function):
            setattr(function, '__sentience__', kwargs)
            return function
        return inner
