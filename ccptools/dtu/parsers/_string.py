__all__ = [
    'str_to_rel',
    'str_to_2dates',
]


from ccptools.dtu.structs import *

DATE_REXEX = re.compile(r'(?P<year>[0]{0,3}[1-9]\d{0,3})[- /.,\\](?P<month>1[012]|0?\d)[- /.,\\](?P<day>3[01]|[012]?\d)')


def str_to_rel(str_value: str) -> Optional[Datetime]:
    """
    """
    str_value = str_value.strip().lower()
    if str_value in ('now', 'today'):
        return Datetime.now()
    elif str_value == 'yesterday':
        return Datetime.now() - TimeDelta(days=1)
    elif str_value == 'tomorrow':
        return Datetime.now() + TimeDelta(days=1)
    else:
        return None


def str_to_2dates(str_value: str) -> Optional[Tuple[Date, Date]]:
    """Converts a string in the format "FROM_DATE SEPERATOR TO_DATE" where
    FROM_DATE and TO_DATE are ISO formatted dates and SEPERATOR is anything and
    turns it into a 2-tuple of python date objects.

    >>> str_to_2dates('1969-08-15 to 1967-08-19')  # Woodstock
    (datetime.date(1969, 8, 15), datetime.date(1967, 8, 19))
    """
    try:
        match = DATE_REXEX.findall(str_value.strip())
        if match:
            if len(match) == 2:  # We want two dates
                if len(match[0]) == 3 and len(match[1]) == 3:  # We want three parts
                    date_from = datetime.date(int(match[0][0]), int(match[0][1]), int(match[0][2]))
                    date_to = datetime.date(int(match[1][0]), int(match[1][1]), int(match[1][2]))
                    return date_from, date_to
        return None
    except Exception:
        return None
