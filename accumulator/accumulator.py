import hashlib
from typing import Union
from .event import Event

NIL = bytes([0] * 32)

def d(n: int) -> int:
    """Return the maximum power of two that divides n. Return 0 for n == 0."""
    return n & (~(n - 1))


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

    return n - d(n)

def H(x: Union[str, bytes]) -> bytes:
    """If x an array of bytes, return the sha256 digest of it.
    If x if a string, convert it to bytes using utf8 encoding first, then return the digest."""
    b = x.encode("utf8") if isinstance(x, str) else x
    return hashlib.sha256(b).digest()


class Accumulator:
    """
    Maintains the public state of the accumulator.
    Allows to add elements that should be in the domain of the hash function H, and can add new
    elements, updating the state of the accumulator accordingly.
    Does not hold enough information to produce proofs; instead, whenever a new element is added,
    notifies all listeners of `element_added` with the new value of the counter, the new element
    and the new root hash of the accumulator.
    """

    def __init__(self):
        self.k = 0
        self.S = [NIL]
        self.element_added = Event()

    def __len__(self):
        """Returns `k`, the total number of elements in this accumulator."""
        return self.k

    def increase_counter(self):
        """Increases the counter before adding a new element, and adds a new slot to S if necessary.
        S is extended if k is a power of 2 before being incremented."""
        if self.k == d(self.k):
            self.S.append(None)
        self.k += 1

    # TODO: find better name
    def get_state(self, i: int) -> bytes:
        """Return the accumulator's value R_i, as long as `i` is the largest number divisible by d(i)
        and not greater than k.
        Return NIL if i == 0.
        """
        return NIL if i == 0 else self.S[zeros(i)]

    def get_root(self) -> bytes:
        """Return the current value of the accumulator."""
        return self.get_state(self.k)

    def add(self, x: bytes) -> bytes:
        """
        Insert the new element `x` into the accumulator.
        """
        self.increase_counter()

        prev_state = self.get_state(self.k - 1)
        other_state = self.get_state(self.k - d(self.k))

        data = x + prev_state + other_state
        result = H(data)

        self.S[zeros(self.k)] = result

        self.element_added.notify(self.k, x, result)
        return result


class Prover:
    def __init__(self, accumulator: Accumulator):
        self.elements = dict([(0, NIL)])
        self.R = dict([(0, NIL)])
        self.accumulator = accumulator
        accumulator.element_added += self.element_added

    def element_added(self, k, x, r):
        self.elements[k] = x
        self.R[k] = r

    def prove(self, j):
        return self.prove_from(len(self.accumulator), j)

    def prove_from(self, i, j):
        assert j <= i
        assert i in self.elements and i - 1 in self.R and pred(i) in self.R

        w = [self.elements[i], self.R[i - 1], self.R[pred(i)]]
        if i > j:
            if pred(i) >= j:
                w += self.prove_from(pred(i), j)
            else:
                w += self.prove_from(i - 1, j)

        return w



# returns True if `w` is a valid proof for the statement that the element at position k is x, starting from element i that has S(i) = h
def verify(Ri, i, j, w, x):
    assert j <= i
    if len(w) < 3:
        print("Witness too short")
        return False

    x_i, R_prev, R_pred = w[0:3]

    # verify that H(x_i|R_prev|R_pred) == Ri
    if H(x_i + R_prev + R_pred) != Ri:
        print("Hash did not match")
        return False

    if i == j:
        return x_i == x
    else:  # i > j
        if pred(i) >= j:
            return verify(R_pred, pred(i), j, w[3:], x)
        else:
            return verify(R_prev, i - 1, j, w[3:], x)


def main():
    N = 100
    acc = Accumulator()
    prover = Prover(acc)
    hashes = [NIL]
    xs = [NIL]
    for i in range(1, N + 1):
        x = H(str(i))
        xs.append(x)
        r = acc.add(x)
        hashes.append(r)

    proof = prover.prove(10)

    verified = verify(hashes[84], 84, 10, proof, xs[10])
    if verified:
        print("Proof passed verification")
    else:
        print("Proof did not pass verification")


if __name__ == "__main__":
    main()
