__all__ = [
    'JsonSerializer',
]

from ._jsonsafe import *
from typing import *
import json


class JsonSerializer(JsonSafeSerializer):
    def serialize(self, obj: Any, indent: int = 4, sort_keys: bool = True) -> str:
        return json.dumps(super().serialize(obj), indent=indent, sort_keys=sort_keys)
