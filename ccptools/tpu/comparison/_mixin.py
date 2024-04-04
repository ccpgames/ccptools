__all__ = [
    'ComparableMixin',
]


class ComparableMixin(object):
    """Mixin class for types that should be comparable.
    Subclasses must implement `__lt__`.
    Other comparison functions can be overridden if desired.
    """
    def __new__(cls, *args):
        obj = object.__new__(cls)
        if not hasattr(obj, '__lt__'):
            raise NotImplementedError('__lt__ must be overridden.')
        return obj

    def __eq__(self, other):
        return not self < other and not other < self

    def __ne__(self, other):
        return self < other or other < self

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not other < self
