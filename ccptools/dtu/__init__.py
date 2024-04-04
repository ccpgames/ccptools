"""This is the main API module of datetimeutils of ccptools.

The intended use case is to go:
```python
from ccptools import dtu
```

And then use `dtu` in your code as it serves as the "official" API of the
package.
"""
from ccptools.dtu.structs import *

from ccptools.dtu.shortcuts import *

from ccptools.dtu.casting import *
from ccptools.dtu.formatting import *
from ccptools.dtu.parsers import *

from ccptools import __version__ as VERSION  # noqa
