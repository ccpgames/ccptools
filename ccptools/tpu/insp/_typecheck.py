__all__ = [
    'check_type',
]
from typing import *
import typing
import sys
import logging
log = logging.getLogger(__name__)

_POST_39 = sys.version_info >= (3, 9)


def check_type(val: Any, type_or_annotation: Any) -> bool:
    def _is_special(toa: Any) -> bool:
        if _POST_39:
            if isinstance(toa, typing._SpecialGenericAlias):  # noqa
                return True
        else:
            return toa._special  # noqa

    if val is None and type_or_annotation is None:
        return True

    m = getattr(type_or_annotation, '__module__', None)
    if m == 'typing':
        if type_or_annotation == Any:
            return True
        if isinstance(type_or_annotation, typing._GenericAlias):  # noqa
            if _is_special(type_or_annotation):  # noqa Not subscripted
                return isinstance(val, type_or_annotation.__origin__)

            else:
                if type_or_annotation.__origin__ == Union:
                    if not type_or_annotation.__args__:
                        return True
                    if Any in type_or_annotation.__args__:
                        return True
                    return isinstance(val, type_or_annotation.__args__)

                elif type_or_annotation.__origin__ in (list, set):  # Check list and set
                    if not isinstance(val, type_or_annotation.__origin__):
                        return False
                    if not type_or_annotation.__args__ or Any in type_or_annotation.__args__:
                        return True
                    for sub_val in val:
                        if not check_type(sub_val, Union[type_or_annotation.__args__]):
                            return False
                    return True  # Should be good now! :)

                elif type_or_annotation.__origin__ == tuple:  # Check tuple!
                    if not isinstance(val, tuple):
                        return False
                    if not type_or_annotation.__args__:
                        return True

                    if type_or_annotation.__args__[-1] is ... and len(type_or_annotation.__args__) == 2:
                        for sub_val in val:
                            if not check_type(sub_val, Union[type_or_annotation.__args__[0]]):
                                return False
                        return True  # Should be good now! :)

                    if len(type_or_annotation.__args__) != len(val):
                        return False

                    for i, sub_val in enumerate(val):
                        if not check_type(sub_val, Union[type_or_annotation.__args__[i]]):
                            return False

                    return True  # Should be good now! :)

                elif issubclass(type_or_annotation.__origin__, Mapping):
                    if not isinstance(val, type_or_annotation.__origin__):
                        return False
                    if not type_or_annotation.__args__ or type_or_annotation.__args__ == (Any, Any):
                        return True

                    for k, v in val.items():
                        if not (check_type(k, Union[type_or_annotation.__args__[0]]) and check_type(v, Union[type_or_annotation.__args__[1]])):
                            return False
                    return True
                else:
                    log.warning('I do not know how to check type %r of typing module:(', type_or_annotation)

        if isinstance(type_or_annotation, TypeVar):
            # TODO(thordurm@ccpgames.com>): Not really tested and supported yet officially...
            # TODO(thordurm@ccpgames.com>): Main issue is nested types (if they don't flatten)
            return check_type(val, Union[type_or_annotation.__constraints__])

    return isinstance(val, type_or_annotation)
