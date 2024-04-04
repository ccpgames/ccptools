__all__ = [
    'decode_bytes',
]

_ENCODINGS_TO_TRY = (
    'utf-8',
    'latin-1',
    'utf-16',
    'utf-32',
    'windows-1252',
    'big5',
    'shift_jis',
    'gb18030',
    'iso-8859-15'
)


def decode_bytes(byte_str: bytes) -> str:
    """Tries to decode a bytes string into a str by trial-and-error, first using
    the default encoding of the current runtime environment, and then by going
    through a list of the most commonly used encodings used at the time of this
    writing, in September 2023, as estimated by ChatGTP 4. :D

    :raises ValueError: If it fails to decode the given bytes using any of the
                        encodings attempted
    """
    try:  # First we try to Decode with default encoding!
        return byte_str.decode()
    except UnicodeDecodeError:
        pass

    # If not, then we go through the list...!
    for enc in _ENCODINGS_TO_TRY:
        try:
            return byte_str.decode(enc)
        except UnicodeDecodeError:
            pass

    # If we reach here, then we've failed to decode :(
    raise ValueError(f'failed to decode bytes to str by trial and error: {byte_str!r}')
