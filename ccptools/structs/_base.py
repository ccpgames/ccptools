"""These are the modules used by most of the code in this package.

This is intended for internal use only and is meant to simplify the otherwise
repetitive importing of the same modules over and over again in most of the
python files here.

I.e. instead of starting most files with the same imports as here, you just go:
```python
from ccptools.structs import *  # This includes the `_base`
```
"""
from typing import *

import abc
import dataclasses
import decimal
import enum
import re
import time
