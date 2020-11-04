import hashlib
from typing import Union

NIL = bytes([0] * 32)

def highest_divisor_power_of_2(n: int) -> int:
    """Return the maximum power of two that divides n. Return 0 for n == 0."""
    return n & (~(n - 1))

def floor_lg(n: int) -> int:
    """Return floor(log_2(n))."""
    r = 0
    t = 1
    while 2 * t <= n:
        t = 2 * t
        r = r + 1
    return r

def ceil_lg(n: int) -> int:
    """Return ceiling(log_2(n))."""
    r = 0
    t = 1
    while t < n:
        t = 2 * t
        r = r + 1
    return r


def is_power_of_2(n: int) -> bool:
    return n & (n - 1) == 0


def largest_power_of_2_less_than(n: int) -> int:
    assert n > 1
    if is_power_of_2(n):
        return n // 2
    else:
        return 1 << floor_lg(n)


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
    """For integers n > m > 0, return the largest number not smaller than m that can be obtained by
    progressively zero-ing the least significant 1 digit in the binary representation of n."""
    while pred(n) >= m:
        n = pred(n)
    return n


def hook_index(n: int, t: int) -> int:
    """For integers n and t, finds the largest number not greater than n such that the binary
    representation of n has exactly t zeros."""
    d = 1 << t
    r = n & ~(d - 1) # zero the last t bits of n
    if n & d != 0:
        return r
    else:
        return (r - 1) & ~(d - 1) # zero the last t bits of r - 1


# from https://stackoverflow.com/questions/15978781/how-to-find-integer-nth-roots
def iroot(k, n):
    """Computes floor(n^(1/k)), that is, the k-th root of n, rounded down to the nearest integer."""
    hi = 1
    while pow(hi, k) < n:
        hi *= 2
    lo = hi // 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        midToK = pow(mid, k)
        if midToK < n:
            lo = mid
        elif n < midToK:
            hi = mid
        else:
            return mid
    if pow(hi, k) == n:
        return hi
    else:
        return lo


def H(x: Union[str, bytes]) -> bytes:
    """If x an array of bytes, return the sha256 digest of it.
    If x if a string, convert it to bytes using utf8 encoding first, then return the digest."""
    b = x.encode("utf8") if isinstance(x, str) else x
    return hashlib.sha256(b).digest()