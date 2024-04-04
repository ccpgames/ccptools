import unittest
from ccptools.legacyapi.typeutils import string as typeutils_string
import json
import os


class StringTests(unittest.TestCase):
    def test_russian(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wideunicode/russian_unicode.txt'), mode='rb') as fin:
            data = json.loads(fin.read())

        t = data['tickets'][0]

        replaced = typeutils_string.replace_wide_unicode(t['description'])
        self.assertEqual(t['description'], replaced)

    def test_dequote(self):
        self.assertEqual('foo', typeutils_string.dequote('"foo"'))
        self.assertEqual('foo', typeutils_string.dequote("'foo'"))
        self.assertEqual('foo', typeutils_string.dequote('foo'))

        self.assertEqual('foo bar', typeutils_string.dequote('"foo bar"'))
        self.assertEqual('foo bar', typeutils_string.dequote("'foo bar'"))
        self.assertEqual('foo bar', typeutils_string.dequote('foo bar'))

        self.assertEqual('', typeutils_string.dequote(''))
        self.assertEqual('', typeutils_string.dequote('""'))
        self.assertEqual('', typeutils_string.dequote("''"))

        self.assertEqual('"foo bar', typeutils_string.dequote('"foo bar'))
        self.assertEqual('foo"', typeutils_string.dequote('foo"'))
        self.assertEqual('"foo\'', typeutils_string.dequote('"foo\''))
        self.assertEqual('\'foo"', typeutils_string.dequote('\'foo"'))

        self.assertEqual('foo$bar', typeutils_string.dequote('$foo$bar$', '$'))
        self.assertEqual('foo$bar', typeutils_string.dequote('#foo$bar#', ['$', '#']))
        self.assertEqual('foo#bar', typeutils_string.dequote('#foo#bar#', ['$', '#']))
        self.assertEqual('"foo"', typeutils_string.dequote('"foo"', ['$', '#']))

        self.assertIsNone(typeutils_string.dequote(None))
        self.assertEqual(42, typeutils_string.dequote(42))
