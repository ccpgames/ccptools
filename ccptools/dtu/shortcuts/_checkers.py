__all__ = [
    'is_past',
    'is_future',
]

from ccptools.dtu.structs import *
from ccptools.dtu.casting import *
from ._aliases import *


def is_past(temporal_object: T_TEMPORAL_VALUE) -> bool:
    """Returns true if the given temporal value is in the past.
    """
    return any_to_datetime(temporal_object) < now()


def is_future(temporal_object: T_TEMPORAL_VALUE) -> bool:
    """Returns true if the given temporal value is in the future.
    """
    return any_to_datetime(temporal_object) > now()

