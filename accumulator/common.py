import hashlib
from typing import Union

NIL = bytes([0] * 32)

def highest_divisor_power_of_2(n: int) -> int:
    """Return the maximum power of two that divides n. Return 0 for n == 0."""
    return n & (~(n - 1))

def is_power_of_2(n: int) -> bool:
    return n & (n - 1) == 0

def H(x: Union[str, bytes]) -> bytes:
    """If x an array of bytes, return the sha256 digest of it.
    If x if a string, convert it to bytes using utf8 encoding first, then return the digest."""
    b = x.encode("utf8") if isinstance(x, str) else x
    return hashlib.sha256(b).digest()