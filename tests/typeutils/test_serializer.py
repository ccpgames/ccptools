import unittest

from ccptools.tpu.structs.serializers import *

from tests.typeutils import sometypes
import decimal
import datetime
from ccptools.legacyapi.typeutils import empty


class Foo:
    def __init__(self, a, b=None):
        self.a = a
        self.b = b


class UniversalSerializerTest(unittest.TestCase):
    def setUp(self):
        self.s = UniversalSerializer()
        
    def test_scalar(self):
        self.assertEqual(1, self.s.serialize(1))
        self.assertEqual(1.2, self.s.serialize(1.2))
        self.assertEqual('foo', self.s.serialize('foo'))
        self.assertEqual(b'foo', self.s.serialize(b'foo'))
        self.assertEqual(True, self.s.serialize(True))
        self.assertEqual(False, self.s.serialize(False))
        self.assertEqual(None, self.s.serialize(None))

    def test_primitive(self):
        self.assertEqual(decimal.Decimal('2.34'), self.s.serialize(decimal.Decimal('2.34')))
        self.assertEqual(datetime.datetime(2024, 4, 3, 12, 45, 21), self.s.serialize(datetime.datetime(2024, 4, 3, 12, 45, 21)))
        self.assertEqual(datetime.time(12, 23, 45), self.s.serialize(datetime.time(12, 23, 45)))
        self.assertEqual(datetime.timedelta(days=5, minutes=6), self.s.serialize(datetime.timedelta(days=5, minutes=6)))

    def test_object(self):
        self.assertDictEqual({'a': 7, 'b': 'bar'}, self.s.serialize(Foo(a=7, b='bar')))
        self.assertDictEqual({'a': 7, 'b': None}, self.s.serialize(Foo(a=7)))

        self.assertDictEqual({'a': 7, 'b': {'a': 'cool', 'b': datetime.datetime(2024, 4, 3, 12, 45, 21)}}, self.s.serialize(Foo(a=7, b=Foo(a='cool', b=datetime.datetime(2024, 4, 3, 12, 45, 21)))))

    def test_iters(self):
        self.assertDictEqual({1: 2, 'a': 'b'}, self.s.serialize({1: 2, 'a': 'b'}))
        self.assertListEqual([1, 2, 3, 'a', 'b'], self.s.serialize([1, 2, 3, 'a', 'b']))
        self.assertListEqual([1, 2, 3, 'a', 'b'], self.s.serialize((1, 2, 3, 'a', 'b')))
        self.assertEqual({1, 2, 3, 'a', 'b'}, set(self.s.serialize({1, 2, 3, 'a', 'b'})))


class JsonSafeSerializerTest(unittest.TestCase):
    def setUp(self):
        self.s = JsonSafeSerializer()

    def test_scalar(self):
        self.assertEqual(1, self.s.serialize(1))
        self.assertEqual(1.2, self.s.serialize(1.2))
        self.assertEqual('foo', self.s.serialize('foo'))
        self.assertEqual('foo', self.s.serialize(b'foo'))
        self.assertEqual(True, self.s.serialize(True))
        self.assertEqual(False, self.s.serialize(False))
        self.assertEqual(None, self.s.serialize(None))

    def test_primitive(self):
        self.assertEqual('2.34', self.s.serialize(decimal.Decimal('2.34')))
        self.assertEqual('2024-04-03T12:45:21',
                         self.s.serialize(datetime.datetime(2024, 4, 3, 12, 45, 21)))
        self.assertEqual('12:23:45', self.s.serialize(datetime.time(12, 23, 45)))
        self.assertEqual(432360.0, self.s.serialize(datetime.timedelta(days=5, minutes=6)))

    def test_object(self):
        self.assertDictEqual({'a': 7, 'b': 'bar'}, self.s.serialize(Foo(a=7, b='bar')))
        self.assertDictEqual({'a': 7, 'b': None}, self.s.serialize(Foo(a=7)))

        self.assertDictEqual({'a': 7, 'b': {'a': 'cool', 'b': '2024-04-03T12:45:21'}},
                             self.s.serialize(Foo(a=7, b=Foo(a='cool', b=datetime.datetime(2024, 4, 3, 12, 45, 21)))))

    def test_iters(self):
        self.assertDictEqual({'1': 2, 'a': 'b'}, self.s.serialize({1: 2, 'a': 'b'}))
        self.assertListEqual([1, 2, 3, 'a', 'b'], self.s.serialize([1, 2, 3, 'a', 'b']))
        self.assertListEqual([1, 2, 3, 'a', 'b'], self.s.serialize((1, 2, 3, 'a', 'b')))
        self.assertEqual({1, 2, 3, 'a', 'b'}, set(self.s.serialize({1, 2, 3, 'a', 'b'})))


class JsonSerializerTest(unittest.TestCase):
    def setUp(self):
        self.s = JsonSerializer()

    def test_scalar(self):
        self.assertEqual('1', self.s.serialize(1))
        self.assertEqual('1.2', self.s.serialize(1.2))
        self.assertEqual('"foo"', self.s.serialize('foo'))
        self.assertEqual('"foo"', self.s.serialize(b'foo'))
        self.assertEqual('true', self.s.serialize(True))
        self.assertEqual('false', self.s.serialize(False))
        self.assertEqual('null', self.s.serialize(None))

    def test_primitive(self):
        self.assertEqual('"2.34"', self.s.serialize(decimal.Decimal('2.34')))
        self.assertEqual('"2024-04-03T12:45:21"',
                         self.s.serialize(datetime.datetime(2024, 4, 3, 12, 45, 21)))
        self.assertEqual('"12:23:45"', self.s.serialize(datetime.time(12, 23, 45)))
        self.assertEqual('432360.0', self.s.serialize(datetime.timedelta(days=5, minutes=6)))

    def test_object(self):
        self.assertEqual("""{
    "a": 7,
    "b": "bar"
}""", self.s.serialize(Foo(a=7, b='bar')))
        self.assertEqual("""{
    "a": 7,
    "b": null
}""", self.s.serialize(Foo(a=7)))

        self.assertEqual("""{
    "a": 7,
    "b": {
        "a": "cool",
        "b": "2024-04-03T12:45:21"
    }
}""", self.s.serialize(Foo(a=7, b=Foo(a='cool', b=datetime.datetime(2024, 4, 3, 12, 45, 21)))))

    def test_iters(self):
        self.assertEqual("""{
    "1": 2,
    "a": "b"
}""", self.s.serialize({1: 2, 'a': 'b'}))
        self.assertEqual("""[
    1,
    2,
    3,
    "a",
    "b"
]""", self.s.serialize([1, 2, 3, 'a', 'b']))
        self.assertEqual("""[
    1,
    2,
    3,
    "a",
    "b"
]""", self.s.serialize((1, 2, 3, 'a', 'b')))

