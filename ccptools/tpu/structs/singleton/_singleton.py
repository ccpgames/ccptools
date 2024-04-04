__all__ = [
    'Singleton',
]

from threading import Lock


class Singleton(type):
    """
    Use:
    from tpu import singleton

    class MyClass(BaseClass, metaclass=singleton.Singleton):
        ...

    """
    __instances = {'lock': Lock()}

    def __call__(cls, *args, **kwargs):
        with cls.__instances['lock']:
            if cls not in cls.__instances:
                cls.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
                setattr(cls.__instances[cls], '_singleton_reload', Singleton.wrapper(cls))
            return cls.__instances[cls]

    @staticmethod
    def wrapper(cls):
        def _singleton_reload():
            try:
                with cls.__instances['lock']:
                    del cls.__instances[cls]
            except KeyError:
                pass
            return cls()
        return _singleton_reload
