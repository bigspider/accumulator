import hashlib
from typing import Union

NIL = bytes([0] * 32)

def highest_divisor_power_of_2(n: int) -> int:
    """Return the maximum power of two that divides n. Return 0 for n == 0."""
    return n & (~(n - 1))

def is_power_of_2(n: int) -> bool:
    return n & (n - 1) == 0


# The number of trailing zeros in the binary representation of n
# also equal to log_2(d(n))
def zeros(n: int) -> int:
    """Return the number of trailing zeros in the binary representation of n.
    Return 0 if n == 0."""

    result = 0
    while n & 1 == 0:
        n = n // 2
        result += 1
    return result

def pred(n: int) -> int:
    """Return the number obtained by zeroing the least significant 1 digit in the binary
    represenation of n. Return 0 if n == 0."""

    return n - highest_divisor_power_of_2(n)

def rpred(n: int, m: int) -> int:
    """For integers n > m > 0, return the largest number not smallr than m thayt can be obtained by
    progressively zero-ing the least significant 1 digit in the binary representation of n."""
    while pred(n) >= m:
        n = pred(n)
    return n

def H(x: Union[str, bytes]) -> bytes:
    """If x an array of bytes, return the sha256 digest of it.
    If x if a string, convert it to bytes using utf8 encoding first, then return the digest."""
    b = x.encode("utf8") if isinstance(x, str) else x
    return hashlib.sha256(b).digest()