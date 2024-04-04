__all__ = [
    'venn',
    'startswith',
    'endswith',
    'has',
    'has_all',
    'has_any',
]

from ccptools.tpu.structs import *


def venn(left: Union[List, Set, Tuple, Dict], right: Union[List, Set, Tuple, Dict]) -> Tuple[List, List, List]:
    """Returns the relative complements and intersections of two lists in a
    three-tuple of lists.

     - The first list contains the relative complements of the right list in
       the left one (i.e. list of values unique to the left list)
     - The second list contains the intersection of left and right (i.e. list
       of values that exist in both left and right)
     - The third list contains the relative complements of the left list in
       the right one (i.e. list of values unique to the right list)

    Another way to think of this is to envision the return values as the left,
    middle and right parts of a Venn diagram made from the left and right input
    or different joins of two tables, i.e. left outer join on left table where
    right is null, inner full and right outer join on right table where left
    is null. :)

    Duplicated values in either input list will be ignored (i.e. repeating
    values only appear once in the output).

    Using a dict (or dict like iterable object) will only use and return the
    keys, ignoring the values.

    :param left: Any iterable that can be turned into a set as the left set
    :type left: list | tuple | set | dict | str | unicode
    :param right: Any iterable that can be turned into a set as the right set
    :type right: list | tuple | set | dict | str | unicode
    :return: A three-tuple of lists (see description)
    :rtype: (list, list, list)
    """
    left = set(left)
    right = set(right)
    return list(left.difference(right)), list(left.intersection(right)), list(right.difference(left))


def startswith(main_list: Union[Tuple[Any], List[Any]], sub_list: Union[Tuple[Any], List[Any]]) -> bool:
    """Returns True if the given main_list starts with the same values
    (in order) as the given sub_list.

    :type sub_list: list | tuple
    :type main_list: list | tuple
    :rtype: bool
    """
    if not sub_list:
        return True

    find_len = len(sub_list)
    search_len = len(main_list)

    if find_len > search_len:
        return False

    found = True
    for i in range(find_len):
        if sub_list[i] != main_list[i]:
            found = False
            break
    return found


def endswith(main_list: Union[Tuple[Any], List[Any]], sub_list: Union[Tuple[Any], List[Any]]) -> bool:
    """Returns True if the given main_list ends with the same values
    (in order) as the given sub_list.

    :type sub_list: list | tuple
    :type main_list: list | tuple
    :rtype: bool
    """
    if not sub_list:
        return True

    find_len = len(sub_list)
    search_len = len(main_list)

    if find_len > search_len:
        return False

    found = True
    for i in range(1, find_len+1):
        if sub_list[-i] != main_list[-i]:
            found = False
            break
    return found


def has(main_list: Union[Tuple[Any], List[Any]], sub_list: Union[Tuple[Any], List[Any]]) -> bool:
    """Returns True if the given main_list has all the same values as the given
    sub_list in sequential order (or "is-ordered-subset").

    :param main_list:
    :type main_list: list | tuple
    :param sub_list:
    :type sub_list: list | tuple
    :return:
    :rtype:
    """
    find_len = len(sub_list)
    search_len = len(main_list)

    if not sub_list:
        return True

    if find_len < search_len:
        first_sym = sub_list[0]
        if find_len > 1:
            idx = -1
            found = False
            stopdex = search_len - find_len
            while not found:
                try:
                    idx = main_list.index(first_sym, idx + 1)
                    if idx > stopdex:
                        return False
                    found = True
                    for i in range(1, find_len):
                        if sub_list[i] != main_list[idx + i]:
                            found = False
                            break
                except ValueError:
                    break
            return found
        else:
            return first_sym in main_list
    elif find_len > search_len:
        return False
    else:
        return find_len == search_len


def has_all(main_list: Union[Tuple[Any], List[Any]], sub_list: Union[Tuple[Any], List[Any]]) -> bool:
    """Returns True if the given main_list contains all the values of the given
    sub_list (in any order).

    :param main_list:
    :type main_list: list | tuple | set | dict
    :param sub_list:
    :type sub_list: list | tuple | set | dict
    :return:
    :rtype:
    """
    if not sub_list:
        return True
    sub_set = set(sub_list)
    main_set = set(main_list)
    return sub_set.issubset(main_set)


def has_any(main_list: Union[Tuple[Any], List[Any]], sub_list: Union[Tuple[Any], List[Any]]) -> bool:
    """Returns true if the given main_list contains any of the values in the
    given sub_list (in any order).

    :param main_list:
    :type main_list: list | tuple | set | dict
    :param sub_list:
    :type sub_list: list | tuple | set | dict
    :return:
    :rtype:
    """
    if not sub_list:
        return True
    sub_set = set(sub_list)
    main_set = set(main_list)
    for val in sub_set:
        if val in main_set:
            return True
    return False
