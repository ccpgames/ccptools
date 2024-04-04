import unittest

from ccptools.legacyapi.typeutils import empty


class EmptyTests(unittest.TestCase):
    def test_empty(self):
        self.assertTrue(True)

    def test_empty_dict(self):
        d = {'foo': 123, 'bar': {'A': 'alpha', 'B': 'beta'}, 'oof': None}
        e = empty.EmptyDict(d)
        self.assertEqual(e['foo'], d['foo'])
        self.assertEqual(e.foo, d['foo'])
        self.assertEqual(e.get('foo', None), d['foo'])
        self.assertEqual(getattr(e, 'foo', None), d['foo'])

        self.assertEqual(e['fool'], empty.Empty)
        self.assertEqual(e.fool, empty.Empty)
        self.assertEqual(getattr(e, 'fool', None), empty.Empty)

        self.assertEqual(e.get('fool', None), None)

    def test_if_empty(self):
        bar = empty.Empty
        foo = bar or None
        self.assertIsNone(foo)

        bar = 0
        foo = bar or None
        self.assertIsNone(foo)

        bar = empty.Empty
        foo = empty.if_empty(bar)
        self.assertIsNone(foo)

        bar = empty.Empty
        foo = empty.if_empty(bar, 0)
        self.assertIsNotNone(foo)
        self.assertEqual(foo, 0)

        bar = 0
        foo = empty.if_empty(bar)
        self.assertIsNotNone(foo)
        self.assertEqual(foo, 0)

        bar = 7
        foo = empty.if_empty(bar)
        self.assertIsNotNone(foo)
        self.assertEqual(foo, 7)

