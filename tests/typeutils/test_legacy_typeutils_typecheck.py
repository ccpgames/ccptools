import unittest
import datetime
import typing

from ccptools.legacyapi.typeutils.insp import check_type

import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Foo(object):
    def __init__(self, alpha=''):
        self.alpha = alpha


class Bar(object):
    def __init__(self, beta=''):
        self.beta = beta


class _Values:
    my_none = None
    my_int = 1
    my_int_empty = 0
    my_float = 1.1
    my_float_empty = 0.0
    my_str = 'a string'
    my_str_empty = ''
    my_bytes = b'byte'
    my_bytes_empty = b''

    my_foo = Foo('foo')
    my_bar = Bar('bar')

    my_list = [1, 2, 3]
    my_list_empty = []
    my_list_of_strings = ['one', 'two', 'three']
    my_list_of_foos = [Foo('one'), Foo('two'), Foo('three')]
    my_list_of_bars = [Bar('eno'), Bar('owt'), Bar('eerht')]
    my_list_of_foobars = [Bar('eno'), Foo('two'), Bar('eerht')]

    my_tuple = (4, 5, 6)
    my_tuple_empty = tuple()
    my_tuple_of_strings = ('four', 'five', 'six')
    my_tuple_of_int_str_byte = (4, 'five', b'three')
    my_tuple_of_2_str = ('first', 'second')
    my_tuple_of_str_foo = ('first', Foo('second'))
    my_tuple_of_str_bar = ('first', Bar('second'))

    my_set = {7, 8, 9}
    my_set_empty = set()
    my_set_of_strings = {'seven', 'eight', 'nine'}
    my_set_of_ints_and_str = {'seven', 8, 'nine'}
    my_set_of_foos = {Foo('seven'), Foo('8'), Foo('nine')}
    my_set_of_bars = {Bar('seven'), Bar('8'), Bar('nine')}
    my_set_of_foobars = {Foo('seven'), Bar('8'), Foo('nine')}

    my_dict = {10: 11, 12: 13}
    my_dict_empty = {}
    my_dict_intstr_optional_foobar = {
        1: None,
        'two': Foo('dos'),
        3: Bar('three'),
    }
    my_dict_of_str_datetimes = {'ten': datetime.datetime(2019, 1, 10, 11, 10, 13),
                                'twelve': datetime.datetime(2019, 1, 13, 14, 15, 16)}

    my_datetime = datetime.datetime(2001, 1, 1, 1, 1, 1)


class _Types:
    type_none = type(None)
    type_int = type(1)
    type_float = type(1.1)
    type_str = type('a string')
    type_bytes = type(b'byte')

    type_foo = type(Foo('foo'))
    type_bar = type(Bar('bar'))

    type_list = type([1, 2, 3])
    type_tuple = type((4, 5, 6))
    type_set = type({7, 8, 9})
    type_dict = type({10: 11, 12: 13})

    type_datetime = type(datetime.datetime(2001, 1, 1, 1, 1, 1))


class _Anotations:
    a_string_optional = typing.Optional[str]
    a_byte_or_string_optional = typing.Optional[typing.Union[str, bytes]]

    a_foo = Foo
    a_foobar_union = typing.Union[Foo, Bar]
    a_foobar_str_union = typing.Union[Foo, Bar, str]
    a_foo_optional = typing.Optional[Foo]
    a_foobar_optional_union = typing.Optional[typing.Union[Foo, Bar]]
    a_foobar_str_optional_union = typing.Optional[typing.Union[Foo, Bar, str]]
    a_foobar_str_optional_union_of_unions = typing.Union[typing.Union[Foo, Bar], typing.Optional[str]]

    a_int_or_float = typing.Union[int, float]
    a_int_or_float_or_string = typing.Union[int, float, str]
    a_int_or_datetime = typing.Union[int, datetime.datetime]

    a_list = list
    a_list_no_param = typing.List
    a_list_of_any = typing.List[typing.Any]
    a_list_of_ints = typing.List[int]
    a_list_of_strings = typing.List[str]
    a_list_of_string_or_ints = typing.List[typing.Union[int, str]]
    a_list_of_foos = typing.List[Foo]
    a_list_of_bars = typing.List[Bar]
    a_list_of_foobars = typing.List[typing.Union[Foo, Bar]]

    a_tuple = tuple
    a_tuple_no_param = typing.Tuple
    a_tuple_of_any = typing.Tuple[typing.Any, ...]  # Is this (x,) or (x, y, ...)???
    a_tuple_of_strings = typing.Tuple[str, ...]
    a_tuple_of_2_strings = typing.Tuple[str, str]
    a_tuple_3_of_int_str_byte = typing.Tuple[int, str, bytes]
    a_tuple_of_str_and_foobars = typing.Tuple[str, typing.Union[Foo, Bar]]

    a_set = set
    a_set_no_param = typing.Set
    a_set_of_any = typing.Set[typing.Any]
    a_set_of_strings = typing.Set[str]
    a_set_of_ints = typing.Set[int]
    a_set_of_ints_or_str = typing.Set[typing.Union[int, str]]
    a_set_of_foobars = typing.Set[typing.Union[Foo, Bar]]

    a_dict = dict
    a_dict_no_param = typing.Dict
    a_dict_of_any = typing.Dict[typing.Any, typing.Any]
    a_dict_of_int_ints = typing.Dict[int, int]
    a_dict_of_intstr_optional_foobars = typing.Dict[typing.Union[int, str], typing.Optional[typing.Union[Foo, Bar]]]
    a_dict_of_str_datetimes = typing.Dict[str, datetime.datetime]


class TypeCheckerTest(unittest.TestCase):
    def test_simple_type_check(self):
        self.assertTrue(check_type(_Values.my_int, _Types.type_int))
        self.assertTrue(check_type(_Values.my_int, int))
        self.assertFalse(check_type(_Values.my_int, _Types.type_float))
        self.assertFalse(check_type(_Values.my_int, _Types.type_str))
        self.assertFalse(check_type(_Values.my_int, _Types.type_bytes))
        self.assertFalse(check_type(_Values.my_int, float))
        self.assertFalse(check_type(_Values.my_int, str))
        self.assertFalse(check_type(_Values.my_int, bytes))

        self.assertFalse(check_type(_Values.my_int, _Types.type_foo))
        self.assertFalse(check_type(_Values.my_int, _Types.type_bar))
        self.assertFalse(check_type(_Values.my_int, _Types.type_list))
        self.assertFalse(check_type(_Values.my_int, _Types.type_tuple))
        self.assertFalse(check_type(_Values.my_int, _Types.type_set))
        self.assertFalse(check_type(_Values.my_int, _Types.type_dict))
        self.assertFalse(check_type(_Values.my_int, _Types.type_datetime))

        self.assertTrue(check_type(_Values.my_float, _Types.type_float))
        self.assertTrue(check_type(_Values.my_float, float))
        self.assertFalse(check_type(_Values.my_float, _Types.type_int))
        self.assertFalse(check_type(_Values.my_float, _Types.type_str))
        self.assertFalse(check_type(_Values.my_float, _Types.type_bytes))
        self.assertFalse(check_type(_Values.my_float, int))
        self.assertFalse(check_type(_Values.my_float, str))
        self.assertFalse(check_type(_Values.my_float, bytes))

        self.assertFalse(check_type(_Values.my_float, _Types.type_foo))
        self.assertFalse(check_type(_Values.my_float, _Types.type_bar))
        self.assertFalse(check_type(_Values.my_float, _Types.type_list))
        self.assertFalse(check_type(_Values.my_float, _Types.type_tuple))
        self.assertFalse(check_type(_Values.my_float, _Types.type_set))
        self.assertFalse(check_type(_Values.my_float, _Types.type_dict))
        self.assertFalse(check_type(_Values.my_float, _Types.type_datetime))

        self.assertTrue(check_type(_Values.my_str, _Types.type_str))
        self.assertTrue(check_type(_Values.my_str, str))
        self.assertFalse(check_type(_Values.my_str, _Types.type_int))
        self.assertFalse(check_type(_Values.my_str, _Types.type_float))
        self.assertFalse(check_type(_Values.my_str, _Types.type_bytes))
        self.assertFalse(check_type(_Values.my_str, int))
        self.assertFalse(check_type(_Values.my_str, float))
        self.assertFalse(check_type(_Values.my_str, bytes))

        self.assertFalse(check_type(_Values.my_str, _Types.type_foo))
        self.assertFalse(check_type(_Values.my_str, _Types.type_bar))
        self.assertFalse(check_type(_Values.my_str, _Types.type_list))
        self.assertFalse(check_type(_Values.my_str, _Types.type_tuple))
        self.assertFalse(check_type(_Values.my_str, _Types.type_set))
        self.assertFalse(check_type(_Values.my_str, _Types.type_dict))
        self.assertFalse(check_type(_Values.my_str, _Types.type_datetime))

        self.assertTrue(check_type(_Values.my_bytes, _Types.type_bytes))
        self.assertTrue(check_type(_Values.my_bytes, bytes))
        self.assertFalse(check_type(_Values.my_bytes, _Types.type_int))
        self.assertFalse(check_type(_Values.my_bytes, _Types.type_float))
        self.assertFalse(check_type(_Values.my_bytes, _Types.type_str))
        self.assertFalse(check_type(_Values.my_bytes, int))
        self.assertFalse(check_type(_Values.my_bytes, float))
        self.assertFalse(check_type(_Values.my_bytes, str))

        self.assertFalse(check_type(_Values.my_bytes, _Types.type_foo))
        self.assertFalse(check_type(_Values.my_bytes, _Types.type_bar))
        self.assertFalse(check_type(_Values.my_bytes, _Types.type_list))
        self.assertFalse(check_type(_Values.my_bytes, _Types.type_tuple))
        self.assertFalse(check_type(_Values.my_bytes, _Types.type_set))
        self.assertFalse(check_type(_Values.my_bytes, _Types.type_dict))
        self.assertFalse(check_type(_Values.my_bytes, _Types.type_datetime))

    def test_none_type_check(self):
        self.assertTrue(check_type(_Values.my_none, _Types.type_none))
        self.assertFalse(check_type(_Values.my_none, _Types.type_int))
        self.assertFalse(check_type(_Values.my_none, _Types.type_float))
        self.assertFalse(check_type(_Values.my_none, _Types.type_str))
        self.assertFalse(check_type(_Values.my_none, _Types.type_bytes))
        self.assertFalse(check_type(_Values.my_none, _Types.type_foo))
        self.assertFalse(check_type(_Values.my_none, _Types.type_bar))
        self.assertFalse(check_type(_Values.my_none, _Types.type_list))
        self.assertFalse(check_type(_Values.my_none, _Types.type_tuple))
        self.assertFalse(check_type(_Values.my_none, _Types.type_set))
        self.assertFalse(check_type(_Values.my_none, _Types.type_dict))
        self.assertFalse(check_type(_Values.my_none, _Types.type_datetime))

    def test_obj_type_check(self):
        self.assertTrue(check_type(_Values.my_foo, _Types.type_foo))
        self.assertFalse(check_type(_Values.my_foo, _Types.type_bar))
        self.assertTrue(check_type(_Values.my_bar, _Types.type_bar))
        self.assertFalse(check_type(_Values.my_bar, _Types.type_foo))

    def test_datetime_type_check(self):
        self.assertTrue(check_type(_Values.my_datetime, _Types.type_datetime))
        self.assertFalse(check_type(_Values.my_datetime, _Types.type_int))
        self.assertFalse(check_type(_Values.my_datetime, _Types.type_bar))
        self.assertFalse(check_type(_Values.my_datetime, _Types.type_tuple))

    def test_list_type_check(self):
        self.assertTrue(check_type(_Values.my_list, _Types.type_list))
        self.assertTrue(check_type(_Values.my_list, list))
        self.assertTrue(check_type(_Values.my_list_empty, _Types.type_list))
        self.assertTrue(check_type(_Values.my_list_empty, list))
        self.assertTrue(check_type(_Values.my_list_of_strings, _Types.type_list))
        self.assertTrue(check_type(_Values.my_list_of_strings, list))
        self.assertFalse(check_type(_Values.my_list, tuple))
        self.assertFalse(check_type(_Values.my_list, dict))
        self.assertFalse(check_type(_Values.my_list, set))
        self.assertFalse(check_type(_Values.my_list, int))
        self.assertFalse(check_type(_Values.my_list, _Types.type_foo))
        self.assertFalse(check_type(_Values.my_list, _Types.type_bar))

        self.assertTrue(check_type(_Values.my_tuple, _Types.type_tuple))
        self.assertTrue(check_type(_Values.my_tuple, tuple))
        self.assertTrue(check_type(_Values.my_tuple_empty, _Types.type_tuple))
        self.assertTrue(check_type(_Values.my_tuple_empty, tuple))
        self.assertTrue(check_type(_Values.my_tuple_of_strings, _Types.type_tuple))
        self.assertTrue(check_type(_Values.my_tuple_of_strings, tuple))
        self.assertTrue(check_type(_Values.my_tuple_of_int_str_byte, _Types.type_tuple))
        self.assertTrue(check_type(_Values.my_tuple_of_int_str_byte, tuple))

        self.assertFalse(check_type(_Values.my_tuple, list))
        self.assertFalse(check_type(_Values.my_tuple, dict))
        self.assertFalse(check_type(_Values.my_tuple, set))
        self.assertFalse(check_type(_Values.my_tuple, int))
        self.assertFalse(check_type(_Values.my_tuple, _Types.type_foo))
        self.assertFalse(check_type(_Values.my_tuple, _Types.type_bar))

        self.assertTrue(check_type(_Values.my_set, _Types.type_set))
        self.assertTrue(check_type(_Values.my_set, set))
        self.assertTrue(check_type(_Values.my_set_empty, _Types.type_set))
        self.assertTrue(check_type(_Values.my_set_empty, set))
        self.assertTrue(check_type(_Values.my_set_of_strings, _Types.type_set))
        self.assertTrue(check_type(_Values.my_set_of_strings, set))

        self.assertFalse(check_type(_Values.my_set, list))
        self.assertFalse(check_type(_Values.my_set, dict))
        self.assertFalse(check_type(_Values.my_set, tuple))
        self.assertFalse(check_type(_Values.my_set, int))
        self.assertFalse(check_type(_Values.my_set, _Types.type_foo))
        self.assertFalse(check_type(_Values.my_set, _Types.type_bar))

        self.assertTrue(check_type(_Values.my_dict, _Types.type_dict))
        self.assertTrue(check_type(_Values.my_dict, dict))
        self.assertTrue(check_type(_Values.my_dict_empty, _Types.type_dict))
        self.assertTrue(check_type(_Values.my_dict_empty, dict))
        self.assertTrue(check_type(_Values.my_dict_of_str_datetimes, _Types.type_dict))
        self.assertTrue(check_type(_Values.my_dict_of_str_datetimes, dict))

        self.assertFalse(check_type(_Values.my_dict, list))
        self.assertFalse(check_type(_Values.my_dict, set))
        self.assertFalse(check_type(_Values.my_dict, tuple))
        self.assertFalse(check_type(_Values.my_dict, int))
        self.assertFalse(check_type(_Values.my_dict, _Types.type_foo))
        self.assertFalse(check_type(_Values.my_dict, _Types.type_bar))

    def test_simple_union_type_check(self):
        self.assertTrue(check_type(_Values.my_int, _Anotations.a_int_or_float))
        self.assertTrue(check_type(_Values.my_float, _Anotations.a_int_or_float))
        self.assertFalse(check_type(_Values.my_str, _Anotations.a_int_or_float))

    def test_optional_type_check(self):
        self.assertTrue(check_type(_Values.my_none, _Anotations.a_string_optional))
        self.assertTrue(check_type(_Values.my_str, _Anotations.a_string_optional))
        self.assertTrue(check_type(None, _Anotations.a_string_optional))
        self.assertTrue(check_type('', _Anotations.a_string_optional))
        self.assertTrue(check_type('Foo', _Anotations.a_string_optional))
        self.assertFalse(check_type(_Values.my_int, _Anotations.a_string_optional))

        self.assertTrue(check_type(_Values.my_none, _Anotations.a_byte_or_string_optional))
        self.assertTrue(check_type(_Values.my_str, _Anotations.a_byte_or_string_optional))
        self.assertTrue(
            check_type(_Values.my_bytes, _Anotations.a_byte_or_string_optional))
        self.assertTrue(
            check_type(_Values.my_bytes_empty, _Anotations.a_byte_or_string_optional))
        self.assertTrue(
            check_type(_Values.my_str_empty, _Anotations.a_byte_or_string_optional))
        self.assertFalse(
            check_type(_Values.my_datetime, _Anotations.a_byte_or_string_optional))

    def test_objects_type_check(self):
        self.assertTrue(check_type(_Values.my_foo, _Anotations.a_foo))
        self.assertFalse(check_type(_Values.my_bar, _Anotations.a_foo))
        self.assertFalse(check_type(_Values.my_none, _Anotations.a_foo))
        self.assertFalse(check_type(_Values.my_str, _Anotations.a_foo))
        self.assertFalse(check_type(_Values.my_int, _Anotations.a_foo))

        self.assertTrue(check_type(_Values.my_foo, _Anotations.a_foobar_union))
        self.assertTrue(check_type(_Values.my_bar, _Anotations.a_foobar_union))
        self.assertFalse(check_type(_Values.my_none, _Anotations.a_foobar_union))
        self.assertFalse(check_type(_Values.my_str, _Anotations.a_foobar_union))
        self.assertFalse(check_type(_Values.my_int, _Anotations.a_foobar_union))

        self.assertTrue(check_type(_Values.my_foo, _Anotations.a_foobar_str_union))
        self.assertTrue(check_type(_Values.my_bar, _Anotations.a_foobar_str_union))
        self.assertFalse(check_type(_Values.my_none, _Anotations.a_foobar_str_union))
        self.assertTrue(check_type(_Values.my_str, _Anotations.a_foobar_str_union))
        self.assertFalse(check_type(_Values.my_int, _Anotations.a_foobar_str_union))

        self.assertTrue(check_type(_Values.my_foo, _Anotations.a_foo_optional))
        self.assertFalse(check_type(_Values.my_bar, _Anotations.a_foo_optional))
        self.assertTrue(check_type(_Values.my_none, _Anotations.a_foo_optional))
        self.assertFalse(check_type(_Values.my_str, _Anotations.a_foo_optional))
        self.assertFalse(check_type(_Values.my_int, _Anotations.a_foo_optional))

        self.assertTrue(check_type(_Values.my_foo, _Anotations.a_foobar_optional_union))
        self.assertTrue(check_type(_Values.my_bar, _Anotations.a_foobar_optional_union))
        self.assertTrue(check_type(_Values.my_none, _Anotations.a_foobar_optional_union))
        self.assertFalse(check_type(_Values.my_str, _Anotations.a_foobar_optional_union))
        self.assertFalse(check_type(_Values.my_int, _Anotations.a_foobar_optional_union))

        self.assertTrue(
            check_type(_Values.my_foo, _Anotations.a_foobar_str_optional_union))
        self.assertTrue(
            check_type(_Values.my_bar, _Anotations.a_foobar_str_optional_union))
        self.assertTrue(
            check_type(_Values.my_none, _Anotations.a_foobar_str_optional_union))
        self.assertTrue(
            check_type(_Values.my_str, _Anotations.a_foobar_str_optional_union))
        self.assertFalse(
            check_type(_Values.my_int, _Anotations.a_foobar_str_optional_union))

        self.assertTrue(
            check_type(_Values.my_foo, _Anotations.a_foobar_str_optional_union_of_unions))
        self.assertTrue(
            check_type(_Values.my_bar, _Anotations.a_foobar_str_optional_union_of_unions))
        self.assertTrue(
            check_type(_Values.my_none, _Anotations.a_foobar_str_optional_union_of_unions))
        self.assertTrue(
            check_type(_Values.my_str, _Anotations.a_foobar_str_optional_union_of_unions))
        self.assertFalse(
            check_type(_Values.my_int, _Anotations.a_foobar_str_optional_union_of_unions))

    def test_lists_type_check(self):
        anote = _Anotations.a_list
        self.assertTrue(check_type(_Values.my_list, anote))
        self.assertTrue(check_type(_Values.my_list_empty, anote))
        self.assertTrue(check_type(_Values.my_list_of_strings, anote))
        self.assertTrue(check_type(_Values.my_list_of_foos, anote))
        self.assertTrue(check_type(_Values.my_list_of_bars, anote))
        self.assertTrue(check_type(_Values.my_list_of_foobars, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_set, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_list_no_param

        self.assertTrue(check_type(_Values.my_list, anote))
        self.assertTrue(check_type(_Values.my_list_empty, anote))
        self.assertTrue(check_type(_Values.my_list_of_strings, anote))
        self.assertTrue(check_type(_Values.my_list_of_foos, anote))
        self.assertTrue(check_type(_Values.my_list_of_bars, anote))
        self.assertTrue(check_type(_Values.my_list_of_foobars, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_set, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_list_of_any

        self.assertTrue(check_type(_Values.my_list, anote))
        self.assertTrue(check_type(_Values.my_list_empty, anote))
        self.assertTrue(check_type(_Values.my_list_of_strings, anote))
        self.assertTrue(check_type(_Values.my_list_of_foos, anote))
        self.assertTrue(check_type(_Values.my_list_of_bars, anote))
        self.assertTrue(check_type(_Values.my_list_of_foobars, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_set, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_list_of_ints

        self.assertTrue(check_type(_Values.my_list, anote))
        self.assertTrue(check_type(_Values.my_list_empty, anote))
        self.assertFalse(check_type(_Values.my_list_of_strings, anote))
        self.assertFalse(check_type(_Values.my_list_of_foos, anote))
        self.assertFalse(check_type(_Values.my_list_of_bars, anote))
        self.assertFalse(check_type(_Values.my_list_of_foobars, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_set, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_list_of_strings

        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertTrue(check_type(_Values.my_list_empty, anote))
        self.assertTrue(check_type(_Values.my_list_of_strings, anote))
        self.assertFalse(check_type(_Values.my_list_of_foos, anote))
        self.assertFalse(check_type(_Values.my_list_of_bars, anote))
        self.assertFalse(check_type(_Values.my_list_of_foobars, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_set, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_list_of_string_or_ints

        self.assertTrue(check_type(_Values.my_list, anote))
        self.assertTrue(check_type(_Values.my_list_empty, anote))
        self.assertTrue(check_type(_Values.my_list_of_strings, anote))
        self.assertFalse(check_type(_Values.my_list_of_foos, anote))
        self.assertFalse(check_type(_Values.my_list_of_bars, anote))
        self.assertFalse(check_type(_Values.my_list_of_foobars, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_set, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_list_of_foos

        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertTrue(check_type(_Values.my_list_empty, anote))
        self.assertFalse(check_type(_Values.my_list_of_strings, anote))
        self.assertTrue(check_type(_Values.my_list_of_foos, anote))
        self.assertFalse(check_type(_Values.my_list_of_bars, anote))
        self.assertFalse(check_type(_Values.my_list_of_foobars, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_set, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_list_of_bars

        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertTrue(check_type(_Values.my_list_empty, anote))
        self.assertFalse(check_type(_Values.my_list_of_strings, anote))
        self.assertFalse(check_type(_Values.my_list_of_foos, anote))
        self.assertTrue(check_type(_Values.my_list_of_bars, anote))
        self.assertFalse(check_type(_Values.my_list_of_foobars, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_set, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_list_of_foobars

        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertTrue(check_type(_Values.my_list_empty, anote))
        self.assertFalse(check_type(_Values.my_list_of_strings, anote))
        self.assertTrue(check_type(_Values.my_list_of_foos, anote))
        self.assertTrue(check_type(_Values.my_list_of_bars, anote))
        self.assertTrue(check_type(_Values.my_list_of_foobars, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_set, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

    def test_tuples_type_check(self):
        anote = _Anotations.a_tuple

        self.assertTrue(check_type(_Values.my_tuple, anote))
        self.assertTrue(check_type(_Values.my_tuple_empty, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_strings, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_int_str_byte, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_2_str, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_str_foo, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_str_bar, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_set, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_tuple_no_param

        self.assertTrue(check_type(_Values.my_tuple, anote))
        self.assertTrue(check_type(_Values.my_tuple_empty, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_strings, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_int_str_byte, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_2_str, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_str_foo, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_str_bar, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_set, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_tuple_of_any

        self.assertTrue(check_type(_Values.my_tuple, anote))
        self.assertTrue(check_type(_Values.my_tuple_empty, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_strings, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_int_str_byte, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_2_str, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_str_foo, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_str_bar, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_set, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_tuple_of_strings

        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertTrue(check_type(_Values.my_tuple_empty, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_strings, anote))
        self.assertFalse(check_type(_Values.my_tuple_of_int_str_byte, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_2_str, anote))
        self.assertFalse(check_type(_Values.my_tuple_of_str_foo, anote))
        self.assertFalse(check_type(_Values.my_tuple_of_str_bar, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_set, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_tuple_of_2_strings

        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_tuple_empty, anote))
        self.assertFalse(check_type(_Values.my_tuple_of_strings, anote))
        self.assertFalse(check_type(_Values.my_tuple_of_int_str_byte, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_2_str, anote))
        self.assertFalse(check_type(_Values.my_tuple_of_str_foo, anote))
        self.assertFalse(check_type(_Values.my_tuple_of_str_bar, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_set, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_tuple_3_of_int_str_byte

        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_tuple_empty, anote))
        self.assertFalse(check_type(_Values.my_tuple_of_strings, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_int_str_byte, anote))
        self.assertFalse(check_type(_Values.my_tuple_of_2_str, anote))
        self.assertFalse(check_type(_Values.my_tuple_of_str_foo, anote))
        self.assertFalse(check_type(_Values.my_tuple_of_str_bar, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_set, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_tuple_of_str_and_foobars

        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_tuple_empty, anote))
        self.assertFalse(check_type(_Values.my_tuple_of_strings, anote))
        self.assertFalse(check_type(_Values.my_tuple_of_int_str_byte, anote))
        self.assertFalse(check_type(_Values.my_tuple_of_2_str, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_str_foo, anote))
        self.assertTrue(check_type(_Values.my_tuple_of_str_bar, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_set, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

    def test_sets_type_check(self):
        anote = _Anotations.a_set

        self.assertTrue(check_type(_Values.my_set, anote))
        self.assertTrue(check_type(_Values.my_set_empty, anote))
        self.assertTrue(check_type(_Values.my_set_of_strings, anote))
        self.assertTrue(check_type(_Values.my_set_of_ints_and_str, anote))
        self.assertTrue(check_type(_Values.my_set_of_foos, anote))
        self.assertTrue(check_type(_Values.my_set_of_bars, anote))
        self.assertTrue(check_type(_Values.my_set_of_foobars, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_set_no_param

        self.assertTrue(check_type(_Values.my_set, anote))
        self.assertTrue(check_type(_Values.my_set_empty, anote))
        self.assertTrue(check_type(_Values.my_set_of_strings, anote))
        self.assertTrue(check_type(_Values.my_set_of_ints_and_str, anote))
        self.assertTrue(check_type(_Values.my_set_of_foos, anote))
        self.assertTrue(check_type(_Values.my_set_of_bars, anote))
        self.assertTrue(check_type(_Values.my_set_of_foobars, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_set_of_any

        self.assertTrue(check_type(_Values.my_set, anote))
        self.assertTrue(check_type(_Values.my_set_empty, anote))
        self.assertTrue(check_type(_Values.my_set_of_strings, anote))
        self.assertTrue(check_type(_Values.my_set_of_ints_and_str, anote))
        self.assertTrue(check_type(_Values.my_set_of_foos, anote))
        self.assertTrue(check_type(_Values.my_set_of_bars, anote))
        self.assertTrue(check_type(_Values.my_set_of_foobars, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_set_of_strings

        self.assertFalse(check_type(_Values.my_set, anote))
        self.assertTrue(check_type(_Values.my_set_empty, anote))
        self.assertTrue(check_type(_Values.my_set_of_strings, anote))
        self.assertFalse(check_type(_Values.my_set_of_ints_and_str, anote))
        self.assertFalse(check_type(_Values.my_set_of_foos, anote))
        self.assertFalse(check_type(_Values.my_set_of_bars, anote))
        self.assertFalse(check_type(_Values.my_set_of_foobars, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_set_of_ints

        self.assertTrue(check_type(_Values.my_set, anote))
        self.assertTrue(check_type(_Values.my_set_empty, anote))
        self.assertFalse(check_type(_Values.my_set_of_strings, anote))
        self.assertFalse(check_type(_Values.my_set_of_ints_and_str, anote))
        self.assertFalse(check_type(_Values.my_set_of_foos, anote))
        self.assertFalse(check_type(_Values.my_set_of_bars, anote))
        self.assertFalse(check_type(_Values.my_set_of_foobars, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_set_of_ints_or_str

        self.assertTrue(check_type(_Values.my_set, anote))
        self.assertTrue(check_type(_Values.my_set_empty, anote))
        self.assertTrue(check_type(_Values.my_set_of_strings, anote))
        self.assertTrue(check_type(_Values.my_set_of_ints_and_str, anote))
        self.assertTrue(check_type(_Values.my_set_of_ints_and_str, anote))
        self.assertFalse(check_type(_Values.my_set_of_foos, anote))
        self.assertFalse(check_type(_Values.my_set_of_bars, anote))
        self.assertFalse(check_type(_Values.my_set_of_foobars, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

        anote = _Anotations.a_set_of_foobars

        self.assertFalse(check_type(_Values.my_set, anote))
        self.assertTrue(check_type(_Values.my_set_empty, anote))
        self.assertFalse(check_type(_Values.my_set_of_strings, anote))
        self.assertFalse(check_type(_Values.my_set_of_ints_and_str, anote))
        self.assertFalse(check_type(_Values.my_set_of_ints_and_str, anote))
        self.assertTrue(check_type(_Values.my_set_of_foos, anote))
        self.assertTrue(check_type(_Values.my_set_of_bars, anote))
        self.assertTrue(check_type(_Values.my_set_of_foobars, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_dict, anote))

    def test_dicts_type_check(self):
        anote = _Anotations.a_dict

        self.assertTrue(check_type(_Values.my_dict, anote))
        self.assertTrue(check_type(_Values.my_dict_empty, anote))
        self.assertTrue(check_type(_Values.my_dict_intstr_optional_foobar, anote))
        self.assertTrue(check_type(_Values.my_dict_of_str_datetimes, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_set, anote))

        anote = _Anotations.a_dict_no_param

        self.assertTrue(check_type(_Values.my_dict, anote))
        self.assertTrue(check_type(_Values.my_dict_empty, anote))
        self.assertTrue(check_type(_Values.my_dict_intstr_optional_foobar, anote))
        self.assertTrue(check_type(_Values.my_dict_of_str_datetimes, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_set, anote))

        anote = _Anotations.a_dict_of_any

        self.assertTrue(check_type(_Values.my_dict, anote))
        self.assertTrue(check_type(_Values.my_dict_empty, anote))
        self.assertTrue(check_type(_Values.my_dict_intstr_optional_foobar, anote))
        self.assertTrue(check_type(_Values.my_dict_of_str_datetimes, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_set, anote))

        anote = _Anotations.a_dict_of_int_ints

        self.assertTrue(check_type(_Values.my_dict, anote))
        self.assertTrue(check_type(_Values.my_dict_empty, anote))
        self.assertFalse(check_type(_Values.my_dict_intstr_optional_foobar, anote))
        self.assertFalse(check_type(_Values.my_dict_of_str_datetimes, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_set, anote))

        anote = _Anotations.a_dict_of_intstr_optional_foobars

        self.assertFalse(check_type(_Values.my_dict, anote))
        self.assertTrue(check_type(_Values.my_dict_empty, anote))
        self.assertTrue(check_type(_Values.my_dict_intstr_optional_foobar, anote))
        self.assertFalse(check_type(_Values.my_dict_of_str_datetimes, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_set, anote))

        anote = _Anotations.a_dict_of_str_datetimes

        self.assertFalse(check_type(_Values.my_dict, anote))
        self.assertTrue(check_type(_Values.my_dict_empty, anote))
        self.assertFalse(check_type(_Values.my_dict_intstr_optional_foobar, anote))
        self.assertTrue(check_type(_Values.my_dict_of_str_datetimes, anote))

        self.assertFalse(check_type(_Values.my_foo, anote))
        self.assertFalse(check_type(_Values.my_str, anote))
        self.assertFalse(check_type(_Values.my_list, anote))
        self.assertFalse(check_type(_Values.my_tuple, anote))
        self.assertFalse(check_type(_Values.my_set, anote))
