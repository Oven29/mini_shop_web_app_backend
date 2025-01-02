import random
import re
from string import hexdigits
from typing import Optional
from unidecode import unidecode


def get_translit(text: str) -> str:
    """
    Generate translit string

    :param text: text for translit
    :return: translit string
    """
    return unidecode(text).replace(' ', '_').lower()


def get_rand_string(length: int, base: Optional[str] = None) -> str:
    """
    Generate random string

    :param length: length of string
    :param base: base for random string. Default is hexdigits
    :return: random string
    """
    return ''.join(random.choice(base or hexdigits) for _ in range(length))


def to_snake_case(text: str) -> str:
    """
    Convert string to snake case

    :param text: text for convert
    :return: snake case string
    """
    return re.sub(r'([a-z])([A-Z])', r'\1_\2', text).lower()
