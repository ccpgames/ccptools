__all__ = [
    'now',
    'now_time',
    'today',
    'ticks',
]

from ccptools.dtu.structs import *
import time


def now() -> Datetime:
    """Shortcut alias to `datetime.datetime.now()`"""
    return Datetime.now()


def now_time() -> Time:
    """Shortcut alias to `datetime.datetime.now().time()`"""
    return Datetime.now().time()


def today() -> Date:
    """Shortcut alias to `datetime.date.today()`"""
    return Date.today()


def ticks() -> float:
    """Shortcut alias to `time.time()`"""
    return time.time()
