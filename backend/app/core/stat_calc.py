"""Gen 1 stat calculation formulas."""

import math


def calc_hp(base: int, level: int = 50) -> int:
    """Calculate HP stat using the Gen 1 formula."""
    return math.floor((base * 2 * level) / 100 + level + 10)


def calc_stat(base: int, level: int = 50) -> int:
    """Calculate a non-HP stat using the Gen 1 formula."""
    return math.floor((base * 2 * level) / 100 + 5)
