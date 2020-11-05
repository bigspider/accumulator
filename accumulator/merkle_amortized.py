from .common import NIL, H
from typing import List

# LEGACY CODE: the Merkle trees in .merkle are more efficient, as they will sometimes have shorter proofs.

# Helper functions for representing a binary tree in a zero-indexed array


def parent(n: int) -> int:
    """Return the index of the parent of the node with a positive index n."""
    return (n - 1) // 2


def left_child(n: int) -> int:
    """Return the left child of a node with non-negative index n."""
    return 2 * n + 1


def right_child(n: int) -> int:
    """Return the right child of a node with non-negative index n."""
    return 2 * n + 2


class MerkleTree:
    """
    Maintains a complete Merkle tree, it is possible to insert leaves or change existing leaves; it
    is not possible to remove leaves. The tree is always kept at the minimum capacity that is a
    power of 2 and is enough to contain all the leaves; for example, if 13 leaves have been added,
    16 nodes are reserved for leaves; leaves for missing values contain NIL. The value of each
    internal node is the hash of the values of the left child, concatenated to the value of the
    right child.
    """
    def __init__(self, elements: List[bytes] = []):
        self.k = len(elements)

        # set current capacity to the smallest power of 2 that is at least len(elements)
        self.capacity = 1
        while self.capacity < self.k:
            self.capacity = self.capacity * 2

        self.nodes = [NIL] * (2 * self.capacity - 1)
        for i in range(len(elements)):
            self.nodes[self.first_leaf + i] = elements[i]
        self.recompute_internal_nodes()

    def __len__(self) -> int:
        """Return the total number of leaves in the tree."""
        return self.k

    @property
    def first_leaf(self) -> int:
        """Return the value of the first node for a leaf in the array."""
        return self.capacity - 1

    def fix_node(self, i: int) -> None:
        """Set the value of the node with index `i` to the hash of the concatenation of the
        two children of i."""
        self.nodes[i] = H(self.nodes[left_child(i)] + self.nodes[right_child(i)])

    def fix_up(self, i: int) -> None:
        """For each node in the ancestry of `i` (not including `i`), execute fix_node."""
        while i > 0:
            i = parent(i)
            self.fix_node(i)

    def recompute_internal_nodes(self) -> None:
        """Recompute all the internal nodes. Cost: O(n)."""
        for i in range(self.first_leaf - 1, -1, -1):
            self.fix_node(i)

    def double_capacity(self) -> None:
        """Doubles the capacity of the tree, moving the leaves down one level and recomputing the
        whole tree. Cost: O(n)."""
        initial_capacity = self.capacity
        initial_first_leaf = self.first_leaf
        self.capacity *= 2

        self.nodes += [NIL] * (2 * initial_capacity)
        for j in range(initial_capacity):
            self.nodes[self.first_leaf + j] = self.nodes[initial_first_leaf + j]

        self.recompute_internal_nodes()

    def add(self, x: bytes) -> None:
        """Add an element as new leaf, and recompute the tree accordingly. Cost O(log n) amortized;
        Cost is O(n) when the capacity needs to be doubled."""
        self.set(self.k, x)

    def set(self, index: int, x: bytes) -> None:
        """
        Set the value of the leaf at position `index` to `x`, recomputing the tree accordingly.
        If `index` == `k`, then a new leaf is added and the tree's capacity is double if needed.'

        Cost: Worst case O(log n) if `index` < `k`. If `index` == `k`, then the cost is amortized
        O(log n), but O(n) in the worst case.
        """
        assert 0 <= index <= self.k

        if index == self.k:
            # add a new leaf
            if self.k == self.capacity:
                self.double_capacity()

            self.k += 1

        leaf = self.first_leaf + index
        self.nodes[leaf] = x
        self.fix_up(leaf)

    def get(self, i: int) -> bytes:
        """Return the value of the leaf with index `i`, where 0 <= i < capacity."""
        return self.nodes[self.first_leaf + i]

    def copy(self):
        """Return an identical copy of this Merkle tree."""
        result = MerkleTree()
        result.k = self.k
        result.capacity = self.capacity
        result.nodes = self.nodes.copy()
        return result

    @property
    def root(self) -> bytes:
        """Return the Merkle root."""
        return self.nodes[0]

    def prove_leaf(self, index: int) -> List[bytes]:
        """Produce a proof of membership for the leaf with index `i`, where 0 <= i < capacity."""
        i = self.first_leaf + index
        proof = []
        while i > 0:
            if index % 2 == 0:
                sibling = i + 1
            else:
                sibling = i - 1
            proof.append(self.nodes[sibling])

            i = parent(i)
            index = index // 2

        return proof


def merkle_proof_verify(root: bytes, size: int, element: bytes, index: int, proof: List[bytes]) -> bool:
    """Verify that `proof` is a valid membership proof for the statement that the leaf with
    index `index` is equal to `element` in the tree with the given Merkle `root`."""
    cur_hash = element
    for h in proof:
        if index % 2 == 0:
            cur_hash = H(cur_hash + h)
        else:
            cur_hash = H(h + cur_hash)

        index = index // 2

    return cur_hash == root
