__all__ = [
    'str_norm',
    'str_norm_eq',
    'maxlen',
    'slugify',
    'dequote',
    'replace_wide_unicode',
]

from ccptools.tpu.string import str_norm
from ccptools.tpu.string import str_norm_eq
from ccptools.tpu.string import maxlen
from ccptools.tpu.string import slugify
from ccptools.tpu.string import dequote


def replace_wide_unicode(string, callback='html'):
    """Redundant in Python 3"""
    return string
