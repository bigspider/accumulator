from typing import List
from .event import Event
from .factory import AbstractAccumulatorFactory, AbstractAccumulatorManager, AbstractProver, AbstractVerifier
from .common import H, NIL, zeros, pred, rpred, hook_index, floor_lg
from .merkle import MerkleTree, merkle_proof_verify, get_proof_size

# This module implements the second construction of the accumulator.
# Each new accumulator value R_k is defined as:
#   R_k = H(x_k || M_(k - 1))
# where M_i is the Merkle tree of all the state variables.

# Cost of update: O(log log n)
# Proof size: O(log n log log n)


class SmartAccumulator(AbstractAccumulatorManager):
    def __init__(self):
        self.k = 0
        self.S = MerkleTree()
        self.element_added = Event()

    def __len__(self):
        """Returns `k`, the total number of elements in this accumulator."""
        return self.k

    def get_state(self, i: int) -> bytes:
        """
        Return the accumulator's value R_i, as long as `i` is the largest number divisible by d(i)
        and not greater than k.
        Return NIL if i == 0.
        """

        return NIL if i == 0 else self.S.get(zeros(i))

    def get_root(self) -> bytes:
        """Return the current value of the accumulator."""
        return self.get_state(self.k)

    def add(self, x: bytes) -> bytes:
        """
        Insert the new element `x` into the accumulator.
        """

        M_k_1 = self.S.root

        self.k += 1

        result = H(x + M_k_1)

        self.S.set(zeros(self.k), result)

        self.element_added.notify(self.k, x, result)
        return result


class SmartProver(AbstractProver):
    """
    Listens to updates from a `SmartAccumulator`, and stores the necessary information to create
    witnesses for any element added to the accumulator after this instance is created.
    """
    def __init__(self, accumulator: SmartAccumulator):
        self.elements = dict([(0, NIL)])
        self.R = dict([(0, NIL)])
        self.accumulator = accumulator
        self.initial_k = accumulator.k
        self.initial_S = accumulator.S.copy()
        accumulator.element_added += self.element_added

    def element_added(self, k: int, x: bytes, r: bytes):
        """Listener for events from the accumulator.
        Records each added element, and the corresponding accumulator value."""
        self.elements[k] = x
        self.R[k] = r

    @classmethod
    def make_tree_indexes(cls, n: int):
        """Constructs indexes of all the R_i that are contained in the state for n."""
        i = 0
        t = 1  # 2**i
        result = []
        while t <= n:
            # find the largest number less than or equal than n that ends with exactly i zeros
            idx = hook_index(n, i)
            result.append(idx)

            i = i + 1
            t = t * 2
        return result

    def make_tree(self, n: int):
        """Constructs the Merkle tree M_n"""
        S = []
        for idx in self.make_tree_indexes(n):
            if idx > self.initial_k:
                # we have seen the value since the creation of this Prover
                S.append(self.R[idx])
            else:
                # unchanged since the creation of this Prover; copy value from the initial_S
                S.append(self.initial_S[zeros(idx)])

        return MerkleTree(S)

    def prove(self, j: int) -> List[bytes]:
        """Produce a witness for the j-th element added to the accumulator"""
        return self.prove_from(len(self.accumulator), j)

    def prove_from(self, i: int, j: int) -> List[bytes]:
        """
        Produce a witness for the j-th element of the accumulator, starting from the root when
        the i-th element was added.
        """

        assert self.initial_k <= j <= i
        assert i in self.elements and i - 1 in self.R and pred(i) in self.R

        # Build the Merkle tree for i - 1
        M_prev = self.make_tree(i - 1)
        w = [self.elements[i], M_prev.root]
        if i > j:
            # make the correct proof using rpred
            i_next = rpred(i - 1, j)
            leaf_index = zeros(i_next)

            w.append(M_prev.get(leaf_index))
            w += M_prev.prove_leaf(leaf_index)

            w += self.prove_from(i_next, j)

        return w


class SmartVerifier(AbstractVerifier):
    def verify(self, Ri: bytes, i: int, j: int, w: List[bytes], x: bytes) -> bool:
        """
        Verify that `w` is a valid proof that the the `j`-th element added to the accumulator is `x`,
        given that the value of the accumulator after the `i`-th element was added is `Ri`.
        """

        assert 1 <= j <= i
        if len(w) < 2:
            print("Witness too short")
            return False

        x_i, M_prev_root = w[0:2]

        # verify that H(x_i||M_prev_root) == Ri
        if H(x_i + M_prev_root) != Ri:
            print("Hash did not match")
            return False

        if i == j:
            return x_i == x
        else:  # i > j
            i_next = rpred(i - 1, j)
            leaf_index = zeros(i_next)
            leaf = w[2]

            merkle_tree_size = 1 + floor_lg(i - 1)
            merkle_proof_size = get_proof_size(merkle_tree_size, leaf_index)
            merkle_proof = w[3:3 + merkle_proof_size]
            w_rest = w[3 + merkle_proof_size:]

            if not merkle_proof_verify(M_prev_root, merkle_tree_size, leaf, leaf_index, merkle_proof):
                print("Merkle proof failed")
                return False

            return self.verify(leaf, i_next, j, w_rest, x)


class SmartAccumulatorFactory(AbstractAccumulatorFactory):
    def create_accumulator(self):
        accumulator_manager = SmartAccumulator()
        prover = SmartProver(accumulator_manager)
        verifier = SmartVerifier()
        return accumulator_manager, prover, verifier
