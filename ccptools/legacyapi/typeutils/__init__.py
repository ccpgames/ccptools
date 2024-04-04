"""
This module provides an API to the `ccptools.tpu` (new Type Utils module)
that is backwards compatible with version 3.5.0.0 of the old `typeutils`
module.

This is done to facilitate the updating of code that uses `typeutils` to use
`ccptools` without requiring too much refactoring.

In most cases where code used something like:
```python
from typeutils import bases
```

One should be able to simply replace that line with:
```python
from ccptools.legacyapi.typeutils import bases
```

And that should just work.
"""