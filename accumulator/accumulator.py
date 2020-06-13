from typing import Union, List
from .event import Event
from .common import H, NIL, highest_divisor_power_of_2 as d, is_power_of_2


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
        if is_power_of_2(self.k):
            self.S.append(None)
        self.k += 1

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
    """
    Listens to updates from an `Accumulator`, and stores the necessary information to create
    witnesses for any element added to the accumulator after this instance is created.
    """
    def __init__(self, accumulator: Accumulator):
        self.elements = dict([(0, NIL)])
        self.R = dict([(0, NIL)])
        self.accumulator = accumulator
        accumulator.element_added += self.element_added

    def element_added(self, k: int, x: bytes, r: bytes):
        """Listener for events from the accumulator.
        Records each added element, and the corresponding accumulator value."""
        self.elements[k] = x
        self.R[k] = r

    def prove(self, j: int) -> List[bytes]:
        """Produce a witness for the j-th element added to the accumulator"""
        return self.prove_from(len(self.accumulator), j)

    def prove_from(self, i: int, j: int) -> List[bytes]:
        """Produce a witness for the j-th element of the accumulator, starting from the root when
        the i-th element was added."""
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
def verify(Ri: bytes, i: int, j: int, w: List[bytes], x: bytes) -> bool:
    """
    Verify that `w` is a valid proof that the the `j`-th element added to the accumulator is `x`,
    given that the value of the accumulator after the `i`-th element was added is `Ri`.
    """
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
