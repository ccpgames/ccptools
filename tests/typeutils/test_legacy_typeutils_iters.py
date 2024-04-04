import unittest

from ccptools.legacyapi.typeutils import iters


class TestVenn(unittest.TestCase):
    def testLists(self):
        left, middle, right = iters.venn([1, 2, 3, 4], [3, 4, 5, 6])
        self.assertListEqual(left, [1, 2])
        self.assertListEqual(middle, [3, 4])
        self.assertListEqual(right, [5, 6])

    def testTuples(self):
        left, middle, right = iters.venn((1, 2, 3, 4), (3, 4, 5, 6))
        self.assertListEqual(left, [1, 2])
        self.assertListEqual(middle, [3, 4])
        self.assertListEqual(right, [5, 6])

    def testDicts(self):
        left, middle, right = iters.venn({1: 'A', 2: 'B', 3: 'C', 4: 'D'}, {3: 'E', 4: 'F', 5: 'G', 6: 'H'})
        self.assertListEqual(left, [1, 2])
        self.assertListEqual(middle, [3, 4])
        self.assertListEqual(right, [5, 6])

    def testStrings(self):
        left, middle, right = iters.venn('ABCD', 'CDEF')
        self.assertSetEqual(set(left), {'A', 'B'})
        self.assertSetEqual(set(middle), {'C', 'D'})
        self.assertSetEqual(set(right), {'E', 'F'})

    def testEmpty(self):
        left, middle, right = iters.venn([], [])
        self.assertListEqual(left, [])
        self.assertListEqual(middle, [])
        self.assertListEqual(right, [])

    def testScrambled(self):
        left, middle, right = iters.venn([3, 1, 2, 4], [6, 4, 5, 3])
        self.assertListEqual(left, [1, 2])
        self.assertListEqual(middle, [3, 4])
        self.assertListEqual(right, [5, 6])

    def testDuplicates(self):
        left, middle, right = iters.venn([1, 2, 3, 3, 4], [3, 4, 5, 6, 6, 6])
        self.assertListEqual(left, [1, 2])
        self.assertListEqual(middle, [3, 4])
        self.assertListEqual(right, [5, 6])

    def testDiff(self):
        left, middle, right = iters.venn([1, 2, 3, 4], [5, 6])
        self.assertListEqual(left, [1, 2, 3, 4])
        self.assertListEqual(middle, [])
        self.assertListEqual(right, [5, 6])

    def testUnion(self):
        left, middle, right = iters.venn([1, 2, 3, 4], [1, 2, 3, 4])
        self.assertListEqual(left, [])
        self.assertListEqual(middle, [1, 2, 3, 4])
        self.assertListEqual(right, [])

    def testLeftEmpty(self):
        left, middle, right = iters.venn([], [1, 2, 3, 4])
        self.assertListEqual(left, [])
        self.assertListEqual(middle, [])
        self.assertListEqual(right, [1, 2, 3, 4])

    def testRightEmpty(self):
        left, middle, right = iters.venn([1, 2, 3, 4], [])
        self.assertListEqual(left, [1, 2, 3, 4])
        self.assertListEqual(middle, [])
        self.assertListEqual(right, [])

    def testNoRight(self):
        left, middle, right = iters.venn([1, 2, 3, 4], [3, 4])
        self.assertListEqual(left, [1, 2])
        self.assertListEqual(middle, [3, 4])
        self.assertListEqual(right, [])

    def testNoLeft(self):
        left, middle, right = iters.venn([3, 4], [1, 2, 3, 4])
        self.assertListEqual(left, [])
        self.assertListEqual(middle, [3, 4])
        self.assertListEqual(right, [1, 2])


class TestListStuff(unittest.TestCase):
    def testLists(self):
        left, middle, right = iters.venn([1, 2, 3, 4], [3, 4, 5, 6])
        self.assertListEqual(left, [1, 2])
        self.assertListEqual(middle, [3, 4])
        self.assertListEqual(right, [5, 6])


class TestDictStuff(unittest.TestCase):
    def test_nested_update(self):
        a = {
            'foo': 1,
            'bar': {
                'rab': {
                    'barbara': 2,
                    'rabbabara': 3
                },
                'ara': 4
            },
            'moo': 'bloo'
        }
        a_nope = {
            'foo': 1,
            'bar': {
                'rab': {
                    'barbara': 2,
                    'rabbabara': 3
                },
                'ara': 4
            },
            'moo': 'bloo'
        }
        b = {
            'foo': 101,
            'bar': {
                'rab': {
                    'barbara': 102,
                    'newbara': 100
                }
            }
        }
        exp_nope = {
            'foo': 101,
            'bar': {
                'rab': {
                    'barbara': 102,
                    'newbara': 100
                }
            },
            'moo': 'bloo'
        }
        exp = {
            'foo': 101,
            'bar': {
                'rab': {
                    'barbara': 102,
                    'rabbabara': 3,
                    'newbara': 100
                },
                'ara': 4
            },
            'moo': 'bloo'
        }

        self.assertNotEqual(exp_nope, a_nope)
        a_nope.update(b)
        self.assertEqual(exp_nope, a_nope)
        self.assertNotEqual(exp, a_nope)

        self.assertNotEqual(exp, a)
        iters.nested_dict_update(a, b)
        self.assertEqual(exp, a)
        self.assertNotEqual(exp_nope, a)

    def test_empty_dict_nested_update(self):
        from ccptools.legacyapi.typeutils import empty
        a = empty.EmptyDict(**{
            'foo': 1,
            'bar': {
                'rab': {
                    'barbara': 2,
                    'rabbabara': 3
                },
                'ara': 4
            },
            'moo': 'bloo'
        })
        a_nope = empty.EmptyDict(**{
            'foo': 1,
            'bar': {
                'rab': {
                    'barbara': 2,
                    'rabbabara': 3
                },
                'ara': 4
            },
            'moo': 'bloo'
        })
        b = {
            'foo': 101,
            'bar': {
                'rab': {
                    'barbara': 102,
                    'newbara': 100
                }
            }
        }
        exp_nope = empty.EmptyDict(**{
            'foo': 101,
            'bar': {
                'rab': {
                    'barbara': 102,
                    'newbara': 100
                }
            },
            'moo': 'bloo'
        })
        exp = empty.EmptyDict(**{
            'foo': 101,
            'bar': {
                'rab': {
                    'barbara': 102,
                    'rabbabara': 3,
                    'newbara': 100
                },
                'ara': 4
            },
            'moo': 'bloo'
        })

        self.assertNotEqual(exp_nope, a_nope)
        a_nope.update(b)
        self.assertEqual(exp_nope, a_nope)
        self.assertNotEqual(exp, a_nope)

        self.assertNotEqual(exp, a)
        iters.nested_dict_update(a, b)
        self.assertEqual(exp, a)
        self.assertNotEqual(exp_nope, a)

    def test_nest_dict(self):

        self.assertEqual({'a': {'b': {'c': 'value'}}}, iters.nest_dict(['a', 'b', 'c'], 'value'))
        self.assertEqual({'a': {'b': {'c': 'value'}}}, iters.str_nest_dict('a.b.c', 'value'))
