from typing import List
from .event import Event
from .common import H, NIL, highest_divisor_power_of_2 as d, is_power_of_2, zeros, pred, rpred, hook_index, floor_lg
from .merkle import MerkleTree, merkle_proof_verify


class SmartAccumulator:
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
        self.S = MerkleTree()
        self.element_added = Event()

    def __len__(self):
        """Returns `k`, the total number of elements in this accumulator."""
        return self.k

    def increase_counter(self):
        """Increases the counter before adding a new element, and adds a new slot to S if necessary.
        S is extended if k is a power of 2 after being incremented."""
        self.k += 1
        if is_power_of_2(self.k):
            self.S.add(NIL)

    def get_state(self, i: int) -> bytes:
        """Return the accumulator's value R_i, as long as `i` is the largest number divisible by d(i)
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

        self.increase_counter()

        result = H(x + M_k_1)

        self.S.set(zeros(self.k), result)

        self.element_added.notify(self.k, x, result)
        return result


class SmartProver:
    """
    Listens to updates from an `Accumulator`, and stores the necessary information to create
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
        t = 1 # 2**i
        I = []
        while t <= n:
            # find the largest number less than or equal than n that ends with exactly i zeros
            idx = hook_index(n, i)
            I.append(idx)

            i = i + 1
            t = t * 2
        return I

    def make_tree(self, n: int):
        """Constructs the Merkle tree M_n"""
        I = self.make_tree_indexes(n)
        S = []
        for idx in I:
            if idx > self.initial_k:
                S.append(self.R[idx]) # we have seen the value since the creation of this Prover
            else:
                S.append(self.initial_S[zeros(idx)]) # unchanged since the creation of this Prover; copy value from the initial_S 

        return MerkleTree(S)

    def prove(self, j: int) -> List[bytes]:
        """Produce a witness for the j-th element added to the accumulator"""
        return self.prove_from(len(self.accumulator), j)

    def prove_from(self, i: int, j: int) -> List[bytes]:
        """Produce a witness for the j-th element of the accumulator, starting from the root when
        the i-th element was added."""
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



# returns True if `w` is a valid proof for the statement that the element at position j is x, starting from element i
# that has accumulator root Ri
def smart_verify(Ri: bytes, i: int, j: int, w: List[bytes], x: bytes) -> bool:
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

        merkle_tree_height = floor_lg(i - 1)
        merkle_proof = w[3:3 + merkle_tree_height]
        w_rest = w[3 + merkle_tree_height:]

        if not merkle_proof_verify(M_prev_root, leaf, leaf_index, merkle_proof):
            print("Merkle proof failed")
            return False
        
        return smart_verify(leaf, i_next, j, w_rest, x)
