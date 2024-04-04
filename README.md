# CCP Games Python Toolkit

A smooshup of a few Python packages from the CCP Tools Team of old (Team 
Batcave).

Our two most commonly used internal packages, called `datetimeutils` and 
`typeutils` were too _generically_ named for Pypi.org and since they were 
both used in something like 80-90% of our other projects, it made sense to 
just smoosh them together in one module, and thus, the `ccptools` package 
was born.

Here's the README of the [Date Time Utils](./ccptools/dtu/README.md) submodule.

Here's the README of the [Type Utils](./ccptools/tpu/README.md) submodule.


## Date-Time Utils

The old `datetimeutils` package is now included here as the `dtu` submodule.

```python
from ccptools import dtu
```

### Changes from `datetimeutils`

The name has been shortened to `dtu` to speed up usage _(although you can 
also just go `from ccptools.dtu import *` if you wish)_.

The code has also been quite heavily refactored but everything that was 
available in `datetimeutils` 2.3.0.0 should be accessible via `ccptools.legacyapi.datetimeutils`.

That is, for a super low-effort upgrade from older `datetimeutils` version 
to the new `ccptools` package, simply replace...:

```python
import datetimeutils
```

...with...

```python
from ccptools.legacyapi import datetimeutils
```

...and everything should work fine! :)

Note that any Python 2.7 support has been removed.

### Changes from `typeutils`

The name has been shortened to `tpu` although that's more to fit in with the 
`dtu` pattern. It shouldn't really matter since `typeutils` was rarely if 
ever imported directly since it was split into multiple submodules from the 
start.

Nevertheless to accommodate any changed from `typeutils` 3.5.0.0 and ease 
migration over to `ccptools` the old API is aliased in 
`ccptools.legacyapi.typeutils`.

So you can simply replace

```python
from typeutils import metas
```

...with...

```python
from ccptools.legacyapi.typeutils import metas
```

...and everything should work fine! :)

Note that any Python 2.7 support has been removed.

## Structs

Importing `*` from the `structs` submodule will import all of the most 
commonly used imports in our projects:
```python
from typing import *  # For type annotation

import abc  # For interfaces (Abstract Base Classes)
import dataclasses  # For dataclass structs
import decimal  # Used whenever we're handling money
import enum  # Also used for struct creation
import re  # Used surprisingly frequently
import time  # Very commonly used
```

Note that datetime is not included in this. That's because tt'll also import 
the aliases from the Datetime Utils (`ccptools.dtu.structs.aliases`) 
package instead:

```python
Date = datetime.date
Time = datetime.time
Datetime = datetime.datetime
TimeDelta = datetime.timedelta
TzInfo = datetime.tzinfo
TimeZone = datetime.timezone
```

Furthermore, it'll also include a few of the most commonly used utility 
classes from the Type Utils submodule, the `Singleton` Meta Class and the 
`Empty` and `EmptyDict` classes as well as the `if_empty` method.

So in most cases we can cover something like 90% of any imports we tend to 
need in every Python file with a single line:

```python
from ccptools.structs import *
```