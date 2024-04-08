__all__ = [
    'EnumEx',
]

import enum
from typing import *

_T_ENUM = TypeVar('_T_ENUM', bound='EnumEx')

_NOT_SUPPLIED = object()


class EnumEx(enum.Enum):
    @classmethod
    def from_any(cls: Type[_T_ENUM], value: Any,
                 default: Union[_T_ENUM, None] = _NOT_SUPPLIED) -> _T_ENUM:
        """Casts any sensible value to an Enum of this type.

        :param value: The value to cast to an Enum
        :param default: Default value to return on failed eval if any. Defaults
                        to _NOT_SUPPLIED and makes this method raise an
                        exception on failure
        """
        from ccptools.tpu.casting import enum_eval
        return enum_eval(value, cls, default=default, raise_on_fail=(default is _NOT_SUPPLIED))
