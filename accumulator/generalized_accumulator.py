from typing import Union, List, Callable
from .event import Event
from .merkle import MerkleTree, get_proof_size, merkle_proof_verify
from .common import H, NIL, highest_divisor_power_of_2 as d, is_power_of_2, zeros, pred, ceil_lg, iroot
from .factory import AbstractAccumulatorFactory, AbstractAccumulatorManager, AbstractProver, AbstractVerifier

# This module implements the generalized, parameterized variant of the simple accumulator.
# Each new accumulator value R_k is defined as:
#   R_k = H(x_k || M_k)
# where M_k is the Merkle root of the vector of a number of accumulators for representative indices.
# The vector of representative elements is sorted by decreasing index, and it must start with R_{k - 1}.
# When generating or verifying a proof for a target element x_j, the leaf of the Merkle tree that is included in the
# proof (or revealed) is the one corresponding to the element with the smallest index which is at least j.

class GeneralizedAccumulator(AbstractAccumulatorManager):
    def __init__(self, get_representatives_fn: Callable[[int], List[int]]):
        self.k = 0
        self.S = [NIL]
        self.element_added = Event()
        self.get_representatives = get_representatives_fn

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

        prev_states = [self.get_state(x) for x in self.get_representatives(self.k)]
        mt = MerkleTree(prev_states)

        result = H(x + mt.root)

        self.S[zeros(self.k)] = result

        self.element_added.notify(self.k, x, result)
        return result


class GeneralizedProver(AbstractProver):
    """
    Listens to updates from a `GeneralizedAccumulator`, and stores the necessary information to create
    witnesses for any element added to the accumulator after this instance is created.
    """
    def __init__(self, get_representatives_fn: Callable[[int], List[int]], accumulator: GeneralizedAccumulator):
        self.elements = dict([(0, NIL)])
        self.R = dict([(0, NIL)])
        self.get_representatives = get_representatives_fn
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

        representatives = self.get_representatives(i)

        assert all(t in self.elements for t in representatives)

        prev_states = [self.R[x] for x in representatives]
        mt = MerkleTree(prev_states)

        w = [self.elements[i], mt.root]

        if i > j:
            next_i = min(rep for rep in representatives if rep >= j)
            leaf_index = next(l for l, val in enumerate(representatives) if val == next_i)
            w.append(mt.get(leaf_index))
            w += mt.prove_leaf(leaf_index)

            w += self.prove_from(next_i, j)

        return w


class GeneralizedVerifier(AbstractVerifier):
    def __init__(self, get_representatives_fn: Callable[[int], List[int]]):
        self.get_representatives = get_representatives_fn

    def verify(self, Ri: bytes, i: int, j: int, w: List[bytes], x: bytes) -> bool:
        """
        Verify that `w` is a valid proof that the the `j`-th element added to the accumulator is `x`,
        given that the value of the accumulator after the `i`-th element was added is `Ri`.
        """
        assert j <= i

        representatives = self.get_representatives(i)

        if len(w) < 2:
            print("Witness too short")
            return False

        x_i, mt_root = w[0:2]

        # verify that the hash of x_i concatenated to all the representatives equals Ri
        if H(x_i + mt_root) != Ri:
            print("Hash did not match")
            return False

        if i == j:
            return x_i == x
        else:  # i > j
            # find the index of the smallest representative that is >= j 
            representatives = self.get_representatives(i)
            next_repr_index = 0
            while next_repr_index < len(representatives) - 1 and representatives[next_repr_index+1] >= j:
                next_repr_index += 1

            merkle_tree_size = len(representatives)
            merkle_proof_size = get_proof_size(merkle_tree_size, next_repr_index)

            leaf = w[2]
            merkle_proof = w[3:3 + merkle_proof_size]
            w_rest = w[3 + merkle_proof_size:]

            if not merkle_proof_verify(mt_root, merkle_tree_size, leaf, next_repr_index, merkle_proof):
                print("Merkle proof failed")
                return False

            return self.verify(leaf, representatives[next_repr_index], j, w_rest, x)


class GeneralizedAccumulatorFactory(AbstractAccumulatorFactory):
    def create_accumulator(self, get_representatives_fn: Callable[[int], List[int]],):
        accumulator_manager = GeneralizedAccumulator(get_representatives_fn)
        prover = GeneralizedProver(get_representatives_fn, accumulator_manager)
        verifier = GeneralizedVerifier(get_representatives_fn)
        return accumulator_manager, prover, verifier