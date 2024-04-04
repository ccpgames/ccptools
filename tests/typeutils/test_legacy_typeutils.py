import unittest

from ccptools.legacyapi.typeutils import comparison
from ccptools.legacyapi.typeutils import casting


class ComparableMixinTests(unittest.TestCase):

    def testComparisons(self):
        class C(comparison.ComparableMixin):
            def __init__(self, v):
                self.v = v
            def __lt__(self, other):
                return self.v < other.v
        self.assertLess(C(-1), C(0))
        self.assertLessEqual(C(-1), C(0))
        self.assertLessEqual(C(0), C(0))
        self.assertEqual(C(0), C(0))
        self.assertNotEqual(C(1), C(0))
        self.assertGreaterEqual(C(0), C(0))
        self.assertGreaterEqual(C(1), C(0))
        self.assertGreater(C(1), C(0))


class TypeUtilsTest(unittest.TestCase):

    def test_int_eval(self):
        def assertEvalTo(value, target):
            self.assertEqual(casting.int_eval(value), target)

        assertEvalTo(1234, 1234)
        assertEvalTo(123456789123456789, 123456789123456789)
        assertEvalTo(1234, 1234)
        assertEvalTo('1234', 1234)
        assertEvalTo('-1234', -1234)
        assertEvalTo('1234.1234', 1234)
        assertEvalTo('1234,1234', 0)
        assertEvalTo('1234..1234', 0)
        assertEvalTo('1234.1234.1234123', 0)
        assertEvalTo(1234.1234, 1234)
        assertEvalTo(1234.9999, 1234)
        assertEvalTo(-1234.1234, -1234)
        assertEvalTo(None, 0)
        self.assertEqual(casting.int_eval(object(), -7), -7)

    def test_float_eval(self):
        def assertEvalTo(value, target):
            self.assertEqual(casting.float_eval(value), target)

        assertEvalTo(1234, 1234.0)
        assertEvalTo(123456789123456789, 1.2345678912345678e+017)
        assertEvalTo('1234', 1234.0)
        assertEvalTo('-1234', -1234.0)
        assertEvalTo('1234.1234', 1234.1234)
        assertEvalTo('123,1234', 0)
        assertEvalTo('1234..1234', 0)
        assertEvalTo('1234.1234.1234123', 0)
        assertEvalTo(1234.1234, 1234.1234)
        assertEvalTo(1234.9999, 1234.9999)
        assertEvalTo(-1234.1234, -1234.1234)
        assertEvalTo(None, 0.0)
        self.assertEqual(casting.float_eval(object(), -7.0), -7.0)

    def test_bool_eval(self):
        def assertEvalTrue(value):
            self.assertTrue(casting.bool_eval(value))

        def assertEvalFalse(value):
            self.assertFalse(casting.bool_eval(value))

        assertEvalTrue(True)
        assertEvalTrue('True')
        assertEvalTrue('TRUE')
        assertEvalTrue('tRuE')
        assertEvalTrue('  trUE  ')
        assertEvalTrue(-1)
        assertEvalTrue(1)
        assertEvalTrue(1234)
        assertEvalTrue(123456789123456789)
        assertEvalTrue('-1234')
        assertEvalTrue('1234')
        assertEvalTrue('-1234.1234')
        assertEvalTrue('1234.1234')
        assertEvalTrue(-1.0)
        assertEvalTrue(-0.00000001)
        assertEvalTrue(0.1)
        assertEvalTrue(0.000000001)
        assertEvalTrue(1234.1234)
        assertEvalTrue(1234.9999)

        assertEvalFalse(False)
        assertEvalFalse('False')
        assertEvalFalse('FALSE')
        assertEvalFalse('fAlSe')
        assertEvalFalse('  falSE  ')
        assertEvalFalse('yomama')
        assertEvalFalse('')
        assertEvalFalse(0)
        assertEvalFalse(object())
        assertEvalFalse('0')
        assertEvalFalse('0.0')
        assertEvalFalse('1234,1234')
        assertEvalFalse('1234..1234')
        assertEvalFalse('1234.1234.1234123')
        assertEvalFalse(0.0)
        assertEvalFalse(None)

    def test_split_bitmask(self):
        def assertSame(value, target):
            self.assertEqual(casting.split_bitmask(value), target)

        assertSame(0, [])
        assertSame(1, [1])
        assertSame(2, [2])
        assertSame(3, [1, 2])
        assertSame(4, [4])
        assertSame(12, [4, 8])
        assertSame(123, [1, 2, 8, 16, 32, 64])
        assertSame(1234, [2, 16, 64, 128, 1024])
        assertSame(12345, [1, 8, 16, 32, 4096, 8192])
        assertSame(123456, [64, 512, 8192, 16384, 32768, 65536])
        assertSame(1234567, [1, 2, 4, 128, 512, 1024, 4096, 16384, 32768, 131072, 1048576])

        assertSame(-1, [])
        assertSame(-12, [])
        assertSame(-1234567890123456789, [])
        assertSame(1, [1])
        assertSame(1234567890123456789, [1, 4, 16, 256, 32768, 65536, 524288, 2097152, 4194304,
                                         8388608, 16777216, 67108864, 134217728, 268435456,
                                         536870912, 1073741824, 17179869184, 68719476736,
                                         137438953472, 274877906944, 549755813888,
                                         17592186044416, 562949953421312, 9007199254740992,
                                         72057594037927936, 1152921504606846976])
