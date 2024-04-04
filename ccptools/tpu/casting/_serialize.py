__all__ = [
    'any_to_json',
]


from ccptools.tpu.structs import *
from ccptools.tpu.structs.serializers import *

_serializer = JsonSerializer()


def any_to_json(anything: Any, skip_keys=None, skip_values=None, skip_private=True, skip_nones=False, skip_empties=False,
                max_depth=0) -> str:
    _serializer.skip_keys = skip_keys
    _serializer.skip_values = skip_values
    _serializer.skip_private = skip_private
    _serializer.skip_nones = skip_nones
    _serializer.skip_empties = skip_empties
    _serializer.max_depth = max_depth
    return _serializer.serialize(anything)
