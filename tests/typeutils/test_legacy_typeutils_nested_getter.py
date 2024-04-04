import unittest

from ccptools.legacyapi.typeutils import iters


class TestNestedGetter(unittest.TestCase):
    def test_nested_getter(self):
        obj = {'a': {'b': {'c': 7}}}

        self.assertEqual(7, iters.nested_get(obj, ('a', 'b', 'c')))

        obj2 = {'a': {'b': [
            {'c': 6},
            {'c': 7},
            {'c': 8}
        ]}}

        self.assertEqual(7, iters.nested_get(obj2, ('a', 'b', 1, 'c')))

        self.assertEqual('banana', iters.nested_get({'a': {7: {'c': ['apple', 'banana', 'cantaloupe']}, 5: 'other'}},
                                                    ('a', 7, 'c', -2)))

    def test_nested_setter(self):
        obj = {'a': {'b': {'c': 7}}}
        exp = {'a': {'b': {'c': 9}}}
        iters.nested_set(obj, ('a', 'b', 'c'), 9)
        self.assertEqual(exp, obj)

        obj2 = {'a': [11, 22, {'c': 7}, 44]}
        exp2 = {'a': [11, 22, {'c': 9}, 44]}
        iters.nested_set(obj2, ('a', 2, 'c'), 9)
        self.assertEqual(exp2, obj2)

        obj3 = {'a': {'notb': 7}}
        exp3 = {'a': {'notb': 7, 'b': {'c': 9}}}
        iters.nested_set(obj3, ('a', 'b', 'c'), 9)
        self.assertEqual(exp3, obj3)

        obj4 = {'a': {'notb': 7}}
        exp4 = {'a': {'notb': 7, 2: {'c': 9}}}
        iters.nested_set(obj4, ('a', 2, 'c'), 9)
        self.assertEqual(exp4, obj4)
