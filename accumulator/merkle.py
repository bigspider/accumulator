from .common import NIL, H
from typing import List

# A dynamic Merkle tree. Can add leafs or change existing leafs, but cannot remove leafs.
# Leafs are already assumed to be in the domain of the hash function. Each internal node is the hash of the concatenation of the two leaves.

# for a tree with n leafs, with adding a leaf is amortized log(n), editing is worst case log(n)

def parent(n: int) -> int:
    return (n - 1) // 2

def left_child(n: int) -> int:
    return 2 * n + 1

def right_child(n: int) -> int:
    return 2 * n + 2

def merge_hashes(h1: bytes, h2: bytes) -> bytes:
    return H(h1 + h2) if h1 < h2 else H(h2 + h1)

class MerkleTree:
    def __init__(self):
        self.k = 0
        self.capacity = 1 # current capacity; always a power of two
        self.nodes = [NIL]

    def __len__(self) -> int:
        """Returns the total number of leafs in the tree."""
        return self.k

    @property
    def first_leaf(self) -> int:
        return self.capacity - 1

    def fix_node(self, i: int) -> None:
        self.nodes[i] = merge_hashes(self.nodes[left_child(i)], self.nodes[right_child(i)])

    def fix_up(self, i: int) -> None:
        while i > 0:
            i = parent(i)
            self.fix_node(i)

    def recompute_internal_nodes(self) -> None:
        for i in range(self.first_leaf - 1, -1, -1):
            self.fix_node(i)

    def double_capacity(self) -> None:
        initial_capacity = self.capacity
        initial_first_leaf = self.first_leaf
        self.capacity *= 2

        self.nodes += [NIL] * (2 * initial_capacity)
        for j in range(initial_capacity):
            self.nodes[self.first_leaf + j] = self.nodes[initial_first_leaf + j]

        self.recompute_internal_nodes()

    def add(self, x: bytes) -> None:
        if self.k == self.capacity:
            self.double_capacity()

        self.k += 1
        self.set(self.k - 1, x)

    def set(self, index: int, x: bytes) -> None:
        leaf = self.first_leaf + index
        self.nodes[leaf] = x
        self.fix_up(leaf)

    def get(self, i: int) -> bytes:
        return self.nodes[self.first_leaf + i]

    @property
    def root(self):
        return self.nodes[0]

    def prove_leaf(self, index: int) -> List[bytes]:
        i = self.first_leaf + index
        proof = [self.nodes[i]]
        while i > 0:
            if index % 2 == 0:
                sibling = i + 1
            else:
                sibling = i - 1
            proof.append(self.nodes[sibling])

            i = parent(i)
            index = index // 2

        return proof


def merkle_proof_verify(root: bytes, proof: List[bytes]) -> bool:
    if len(proof) < 2:
        return False

    i = proof[0]

    h = proof[0]
    for l in proof[1:]:
        h = merge_hashes(h, l)

    return h == root
