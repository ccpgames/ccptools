__all__ = [
    'split_bitmask',
]


def split_bitmask(composite_value):
    """Takes an int or long value representing a composite bitmask and returns
    a list of the individual bit flag values contained in the mask.

    Put another way, this splits a number into it's "power-of-two" components.

    Examples:
    ---------

        >>> split_bitmask(1)
        [1]
        >>> split_bitmask(12)
        [4, 8]
        >>> split_bitmask(123)
        [1, 2, 8, 16, 32, 64]

    :param composite_value:
    :type composite_value:
    :return:
    :rtype:
    """
    buff = []
    bitval = 1
    while composite_value > 0:
        if composite_value & 1:
            buff.append(bitval)
        bitval *= 2
        composite_value >>= 1
    return buff
