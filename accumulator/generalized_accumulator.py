from typing import Union, List
from .event import Event
from .common import H, NIL, highest_divisor_power_of_2 as d, is_power_of_2, zeros, pred, ceil_lg, iroot
from .factory import AbstractAccumulatorFactory, AbstractAccumulatorManager, AbstractProver, AbstractVerifier

# This module implements the generalized, parameterized variant of the simple accumulator.
# Each new accumulator value R_k is defined as:
#   R_k = H(x_k || R_1 || R_{a_1} || .. || R_{a_p})
# for p opportunely defined indices that are parte of the special set. TODO: precise definition

# Cost of update: O(p)
# Proof size: O((log n)^(1 + 1/p))

def get_representatives(k: int, p: int):
    if k == 1:
        return []

    # if k is even, we also add k - 1
    result = [k - 1] if k % 2 == 0 else []

    d = iroot(ceil_lg(k), p)
    t = k
    for i in range(p):
        t = pred(t)
        if t == 0:
            break
        result.append(t)
    return result


class GeneralizedAccumulator(AbstractAccumulatorManager):
    def __init__(self, p: int):
        self.k = 0
        self.S = [NIL]
        self.element_added = Event()
        self.p = p

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
        """Insert the new element `x` into the accumulator."""
        self.increase_counter()

        prev_states = [self.get_state(x) for x in get_representatives(self.k, self.p)]

        data = x + b''.join(prev_states)
        result = H(data)

        self.S[zeros(self.k)] = result

        self.element_added.notify(self.k, x, result)
        return result


class GeneralizedProver(AbstractProver):
    """
    Listens to updates from a `GeneralizedAccumulator`, and stores the necessary information to create
    witnesses for any element added to the accumulator after this instance is created.
    """
    def __init__(self, p: int, accumulator: GeneralizedAccumulator):
        self.elements = dict([(0, NIL)])
        self.R = dict([(0, NIL)])
        self.p = p
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

        prev_states = [self.R[x] for x in get_representatives(i, self.p)]
        w = [self.elements[i], *prev_states]

        representatives = get_representatives(i, self.p)
        if i > j:
            next_i = min(rep for rep in representatives if rep >= j)
            w += self.prove_from(next_i, j)

        return w


class GeneralizedVerifier(AbstractVerifier):
    def __init__(self, p: int):
        self.p = p

    def verify(self, Ri: bytes, i: int, j: int, w: List[bytes], x: bytes) -> bool:
        """
        Verify that `w` is a valid proof that the the `j`-th element added to the accumulator is `x`,
        given that the value of the accumulator after the `i`-th element was added is `Ri`.
        """
        assert j <= i

        representatives = get_representatives(i, self.p)

        if len(w) < 1 + len(representatives):
            print("Witness too short")
            return False

        x_i = w[0]
        R_repr = w[1:1 + len(representatives)]

        # verify that the hash of x_i concatenated to all the representatives equals Ri
        if H(x_i + b''.join(R_repr)) != Ri:
            print("Hash did not match")
            return False

        if i == j:
            return x_i == x
        else:  # i > j
            # find the index of the smallest representative that is >= j 
            next_repr_index = 0
            while next_repr_index < len(representatives) - 1 and representatives[next_repr_index+1] >= j:
                next_repr_index += 1

            next_R_i = R_repr[next_repr_index]
            next_i = representatives[next_repr_index]

            return self.verify(next_R_i, next_i, j, w[1 + len(representatives):], x)


class GeneralizedAccumulatorFactory(AbstractAccumulatorFactory):
    def create_accumulator(self, p: int):
        accumulator_manager = GeneralizedAccumulator(p)
        prover = GeneralizedProver(p, accumulator_manager)
        verifier = GeneralizedVerifier(p)
        return accumulator_manager, prover, verifier