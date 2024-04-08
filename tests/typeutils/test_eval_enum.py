import unittest

from ccptools.tpu import casting
import enum

from ccptools.tpu.structs.enumex._enumextra import EnumEx


class TestEnumEval(unittest.TestCase):
    def test_enum_eval(self):
        class SomeEnum(enum.Enum):
            ALPHA = 0
            BETA = 1
            DELTA = 2

        class OtherEnum(enum.Enum):
            ONE = 1
            TWO = 2
            THREE = 3

        self.assertEqual(SomeEnum.ALPHA, casting.enum_eval('ALPHA', SomeEnum))
        self.assertEqual(SomeEnum.ALPHA, casting.enum_eval('Alpha', SomeEnum))
        self.assertEqual(SomeEnum.ALPHA, casting.enum_eval('alPHa ', SomeEnum))
        self.assertEqual(SomeEnum.ALPHA, casting.enum_eval('0 ', SomeEnum))
        self.assertEqual(SomeEnum.ALPHA, casting.enum_eval(0, SomeEnum))
        self.assertEqual(SomeEnum.ALPHA, casting.enum_eval('Yomama', SomeEnum, SomeEnum.ALPHA))
        self.assertIsNone(casting.enum_eval('Yomama', SomeEnum, None))

        self.assertEqual(SomeEnum.DELTA, casting.enum_eval('DELTA', SomeEnum))
        self.assertEqual(SomeEnum.DELTA, casting.enum_eval('Delta', SomeEnum))
        self.assertEqual(SomeEnum.DELTA, casting.enum_eval(' DeLtA  ', SomeEnum))
        self.assertEqual(SomeEnum.DELTA, casting.enum_eval('2 ', SomeEnum))
        self.assertEqual(SomeEnum.DELTA, casting.enum_eval('0b10', SomeEnum))
        self.assertEqual(SomeEnum.DELTA, casting.enum_eval(0b10, SomeEnum))
        self.assertEqual(SomeEnum.DELTA, casting.enum_eval(2, SomeEnum))
        self.assertEqual(SomeEnum.DELTA, casting.enum_eval(OtherEnum.TWO, SomeEnum))
        self.assertEqual(SomeEnum.DELTA, casting.enum_eval('Yomama', SomeEnum, SomeEnum.DELTA))
        self.assertIsNone(casting.enum_eval('Yomama', SomeEnum, None))

    def test_enum_ex(self):
        class SomeEnum(EnumEx):
            ALPHA = 0
            BETA = 1
            DELTA = 2

        class OtherEnum(EnumEx):
            ONE = 1
            TWO = 2
            THREE = 3

        self.assertEqual(SomeEnum.ALPHA, SomeEnum.from_any('ALPHA'))
        self.assertEqual(SomeEnum.ALPHA, SomeEnum.from_any('Alpha'))
        self.assertEqual(SomeEnum.ALPHA, SomeEnum.from_any('alPHa '))
        self.assertEqual(SomeEnum.ALPHA, SomeEnum.from_any('0 '))
        self.assertEqual(SomeEnum.ALPHA, SomeEnum.from_any(0))
        self.assertEqual(SomeEnum.ALPHA, SomeEnum.from_any('Yomama', SomeEnum.ALPHA))
        self.assertIsNone(SomeEnum.from_any('Yomama', None))

        self.assertEqual(SomeEnum.DELTA, SomeEnum.from_any('DELTA'))
        self.assertEqual(SomeEnum.DELTA, SomeEnum.from_any('Delta'))
        self.assertEqual(SomeEnum.DELTA, SomeEnum.from_any(' DeLtA  '))
        self.assertEqual(SomeEnum.DELTA, SomeEnum.from_any('2 '))
        self.assertEqual(SomeEnum.DELTA, SomeEnum.from_any('0b10'))
        self.assertEqual(SomeEnum.DELTA, SomeEnum.from_any(0b10))
        self.assertEqual(SomeEnum.DELTA, SomeEnum.from_any(2))
        self.assertEqual(SomeEnum.DELTA, SomeEnum.from_any(OtherEnum.TWO))
        self.assertEqual(SomeEnum.DELTA, SomeEnum.from_any('Yomama', SomeEnum.DELTA))
        self.assertIsNone(SomeEnum.from_any('Yomama', None))
