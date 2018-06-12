import re

WORD_PATTERN = re.compile("[a-zA-Z]+")
INTEGER_PATTERN = re.compile("[-]?[0-9]+")


def is_word(s):
    """Check if a string is a normal English word."""
    return True if WORD_PATTERN.fullmatch(s) else False


def is_integer(s):
    """Check if a string is a normal Integer."""
    return True if INTEGER_PATTERN.fullmatch(s) else False


if __name__ == "__main__":
    s1 = "1233"
    s2 = "sdfa2"
    s3 = "SEda"
    s4 = ''
    s5 = 'n'

    assert is_word(s1) is False
    assert is_word(s2) is False
    assert is_word(s3) is True
    assert is_word(s4) is False
    assert is_word(s5) is True

    s6 = "-3655"

    assert is_integer(s1) is True
    assert is_integer(s2) is False
    assert is_integer(s4) is False
    assert is_integer(s6) is True

    print("All tests passed!")
