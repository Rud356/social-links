import re

whitespace_re = re.compile(r"[\x00-\x20]")
whitespaces_re = re.compile(r"[\x00-\x20]+")


def squeeze(value: str):
    # Taken from:
    # https://github.com/tornadoweb/tornado/blob/ac85f4f550661af60c5f49c35b3b3111c7c8891a/tornado/escape.py#L86
    """Replace all sequences of whitespace chars with a single space."""
    return whitespaces_re.sub(" ", value).strip()
