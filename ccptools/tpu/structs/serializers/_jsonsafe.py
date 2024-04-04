__all__ = [
    'JsonSafeSerializer',
]

from ._universal import *
from ccptools._common._decode import decode_bytes


class JsonSafeSerializer(UniversalSerializer):
    """
    A version of the UniversalSerializer that serializes types from the datetime
    and decimal modules into JSON safe types.
    """

    def _serialize_maps(self, obj):
        """We need to ensure that all keys are strings, otherwise "sort_keys" in json dumping will fail.
        """
        d = {}
        for k, v in obj.items():
            k = str(k)  # Keys need to be strings in JSON
            if k in self.skip_keys or v in self.skip_values:
                continue
            if self.skip_private and k.startswith('_'):
                continue
            if self.skip_nones and v is None:
                continue
            val = self._serialize_any(v)
            if self.skip_empties and isinstance(val, self._emptyables) and not val:
                continue
            d[k] = val
        return d

    def _serialize_bytes(self, obj):
        return decode_bytes(obj)

    def _serialize_decimal(self, obj):
        """
        :type obj: decimal.Decimal
        :rtype: str
        """
        return '%s' % obj.normalize()

    def _serialize_datetime(self, obj):
        """
        :type obj: datetime.date
        :rtype: str
        """
        return obj.isoformat()

    def _serialize_time(self, obj):
        """
        :type obj: datetime.time
        :rtype: str
        """
        return obj.isoformat()

    def _serialize_date(self, obj):
        """
        :type obj: datetime.date
        :rtype: str
        """
        return obj.isoformat()

    def _serialize_timedelta(self, obj):
        """
        :type obj: datetime.timedelta
        :rtype: float
        """
        return obj.total_seconds()
