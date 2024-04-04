import unittest

from ccptools.legacyapi.typeutils import bases

import io

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log_stream = io.StringIO()
log.addHandler(logging.StreamHandler(stream=log_stream))


class Foo(bases.AttributeFluidObject):
    def __init__(self, bar='BAR', **kwargs):
        self.bar = bar
        super(Foo, self).__init__(**kwargs)


class Bar(bases.AttributeFluidObject):
    _default_value = 'Nothing here!'
    _log_missing_attributes = True
    _logger = log

    def __init__(self, foo='FOO', **kwargs):
        self.foo = foo
        super(Bar, self).__init__(**kwargs)


class FooToo(bases.AttributeFluidObject):
    def __init__(self, bar2='BAR2', **kwargs):
        self.bar2 = bar2
        super(FooToo, self).__init__(**kwargs)


class AttributeFluidObjectTests(unittest.TestCase):
    def test_foo(self):
        f = Foo(bar='BARBAR', alpha='A')
        f.beta = 'B'
        self.assertEqual('BARBAR', f.bar)
        self.assertEqual('A', f.alpha)
        self.assertEqual('B', f.beta)
        self.assertEqual(None, f.delta)

    def test_bar(self):
        b = Bar(foo='FOOYOO', alpha=1)
        b.beta = 2
        self.assertEqual('FOOYOO', b.foo)
        self.assertEqual(1, b.alpha)
        self.assertEqual(2, b.beta)
        self.assertEqual('Nothing here!', b.delta)

    def test_footoo(self):
        f = FooToo(bar2='BARBAR22', alpha='alphaalpha')
        f.beta = 'betabeta'
        self.assertEqual('BARBAR22', f.bar2)
        self.assertEqual('alphaalpha', f.alpha)
        self.assertEqual('betabeta', f.beta)
        self.assertEqual(None, f.delta)

    def test_z_log_stream(self):
        print('log_stream=%r' % log_stream)
        log_stream.seek(0)
        expected = [
            'Attribute "alpha" of Class "Bar" does not exist! Setting it to default value=\'Nothing here!\'',
            'Attribute "beta" of Class "Bar" does not exist! Setting it to default value=\'Nothing here!\'',
            'Attribute "delta" of Class "Bar" does not exist! Setting it to default value=\'Nothing here!\'',
        ]
        lines = log_stream.readlines()
        self.assertEqual(len(expected), len(lines))

        for i, line in enumerate(lines):
            self.assertEqual(line.strip(), expected[i])
