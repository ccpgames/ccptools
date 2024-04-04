import unittest

from ccptools.legacyapi.typeutils import casting


class TestParseParams(unittest.TestCase):
    def test_simple(self):
        params = casting.parse_params(['foo', 'bar=7', 'verbal'], ['debug', 'verbal'])
        self.assertEqual(casting.Params(['foo'], {'bar': '7'}, {'debug': False, 'verbal': True}), params)
        params = casting.parse_params(['foo', 'bar="7"', 'verbal'], ['debug', 'verbal'])
        self.assertEqual(casting.Params(['foo'], {'bar': '7'}, {'debug': False, 'verbal': True}), params)
        params = casting.parse_params(['"foo"', 'bar="7"', 'verbal'], ['debug', 'verbal'])
        self.assertEqual(casting.Params(['foo'], {'bar': '7'}, {'debug': False, 'verbal': True}), params)

    def test_prop_as_kw(self):
        params = casting.parse_params(['foo', 'bar=7', 'verbal'], ['debug', 'verbal'], {'level': ['info', 'warning', 'error']})
        self.assertEqual(casting.Params(['foo'], {'bar': '7', 'level': None}, {'debug': False, 'verbal': True}), params)

        params = casting.parse_params(['foo', 'bar=7', 'verbal', 'warning'], ['debug', 'verbal'], {'level': ['info', 'warning', 'error']})
        self.assertEqual(casting.Params(['foo'], {'bar': '7', 'level': 'warning'}, {'debug': False, 'verbal': True}), params)

        params = casting.parse_params(['foo', 'error', 'bar=7', 'verbal', 'warning'], ['debug', 'verbal'], {'level': ['info', 'warning', 'error']})
        self.assertEqual(casting.Params(['foo'], {'bar': '7', 'level': 'error'}, {'debug': False, 'verbal': True}), params)
