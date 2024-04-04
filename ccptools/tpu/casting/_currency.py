__all__ = [
    'parse_currency_text',
]

from ccptools.tpu.structs import *


_CURRENCY_REGEX = re.compile(r'(?i)^(?P<curr1>(?:[^0-9 \+\-])*)? *(?P<sign1>[\+\-])? *(?P<amount>(?:[0-9]|[\.\,])+) *(?P<sign2>[\+\-])? *(?P<curr2>(?:[^0-9 \+\-])*)?$')


def parse_currency_text(text: str) -> Tuple[Optional[str], Optional[float]]:
    """Parses a text in the form "CURRENCY (+|-) AMOUNT" into a two-tuple of string and float if possible.

    :param text:
    :type text:
    :return:
    :rtype:
    """
    from ccptools.tpu.casting import float_eval
    m = _CURRENCY_REGEX.match(text)
    if m:
        currency = ''
        curr1 = m.group('curr1')
        curr2 = m.group('curr2')
        if curr1:
            if curr2:
                if curr1.lower() == curr2.lower():
                    currency = curr1
                else:
                    currency = '%s/%s' % (curr1, curr2)
            else:
                currency = curr1
        elif curr2:
            currency = curr2

        neg = False
        sign1 = m.group('sign1')
        sign2 = m.group('sign2')
        if sign1 and sign1 == '-':
            neg = True
        elif sign2 and sign2 == '-':
            neg = True

        amount = 0.0
        amount_text = m.group('amount').replace(',', '')
        if amount_text:
            amount = float_eval(amount_text)
        if neg:
            amount = -amount
        return currency, amount

    return None, None
