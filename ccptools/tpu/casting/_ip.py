__all__ = [
    'ip_to_int',
    'int_to_ip',
]


def ip_to_int(ip):
    """

    :param ip:
    :type ip: str
    :return:
    :rtype: int
    :raises ValueError: If the given string is not a valid IP address
    """
    parts = ip.split('.')
    if len(parts) != 4:
        raise ValueError('Not a valid IP address')
    i = 0

    ii = int(parts[0])
    if ii < 0 or ii > 255:
        raise ValueError('Not a valid IP address')
    i += ii << 24

    ii = int(parts[1])
    if ii < 0 or ii > 255:
        raise ValueError('Not a valid IP address')
    i += ii << 16

    ii = int(parts[2])
    if ii < 0 or ii > 255:
        raise ValueError('Not a valid IP address')
    i += ii << 8

    ii = int(parts[3])
    if ii < 0 or ii > 255:
        raise ValueError('Not a valid IP address')
    i += ii

    return i


def int_to_ip(i):
    """

    :param i:
    :type i: int
    :return:
    :rtype: str
    """
    d = i & 0xFF
    i >>= 8
    c = i & 0xFF
    i >>= 8
    b = i & 0xFF
    a = i >> 8
    return '%s.%s.%s.%s' % (a, b, c, d)
