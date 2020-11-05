from accumulator.common import H, NIL
from accumulator.merkle_amortized import MerkleTree, merkle_proof_verify

import unittest

plain_elements = ["some", "small", "list", "of", "distinct", "elements"]
elements = [H(el) for el in plain_elements]


class MerkleTestSuite(unittest.TestCase):
    """Merkle tree implementation test cases."""

    def assertMerkleTreesEqual(self, mt1, mt2):
        """Checks that `mt1` and `mt2` are identically equal MerkleTrees"""
        self.assertEqual(mt1.k, mt2.k)
        self.assertEqual(mt1.capacity, mt2.capacity)
        self.assertEqual(len(mt1.nodes), len(mt2.nodes))
        for j in range(len(mt1.nodes)):
            self.assertEqual(mt1.nodes[j], mt2.nodes[j])

    def test_add_1(self):
        merkle_tree = MerkleTree()
        self.assertEqual(len(merkle_tree), 0)
        merkle_tree.add(elements[0])
        self.assertEqual(len(merkle_tree), 1)
        self.assertEqual(merkle_tree.get(0), elements[0])

    def test_add_2(self):
        merkle_tree = MerkleTree()
        merkle_tree.add(elements[0])
        merkle_tree.add(elements[1])
        self.assertEqual(len(merkle_tree), 2)
        self.assertEqual(merkle_tree.get(0), elements[0])
        self.assertEqual(merkle_tree.get(1), elements[1])

    def test_set(self):
        new_el = H("something new")
        for i in range(len(elements)):
            # check if the Merkle trees obtained by adding the first i elements, and then setting the i
            # or constructing directing with the first i elements, are identical.
            mt1 = MerkleTree(elements)
            mt1.set(i, new_el)

            elements_modified = elements[:i] + [new_el] + elements[i+1:]
            mt2 = MerkleTree(elements_modified)

            self.assertMerkleTreesEqual(mt1, mt2)

    def test_add_many(self):
        merkle_tree = MerkleTree()
        for i in range(len(elements)):
            merkle_tree.add(elements[i])
            self.assertEqual(len(merkle_tree), i + 1)
            self.assertEqual(merkle_tree.get(i), elements[i])

    def test_set_k(self):
        # tests that setting the k-th element has exactly the same effect as adding a new element
        mt1 = MerkleTree()
        mt2 = MerkleTree()
        for i in range(len(elements)):
            mt1.add(elements[i])
            mt2.set(mt2.k, elements[i])
            self.assertMerkleTreesEqual(mt1, mt2)

    def test_capacity(self):
        merkle_tree = MerkleTree()
        self.assertEqual(merkle_tree.capacity, 1)
        merkle_tree.add(elements[0])
        self.assertEqual(merkle_tree.capacity, 1)
        merkle_tree.add(elements[1])
        self.assertEqual(merkle_tree.capacity, 2)
        merkle_tree.add(elements[2])
        self.assertEqual(merkle_tree.capacity, 4)
        merkle_tree.add(elements[3])
        self.assertEqual(merkle_tree.capacity, 4)
        merkle_tree.add(elements[4])
        self.assertEqual(merkle_tree.capacity, 8)
        merkle_tree.add(elements[5])
        self.assertEqual(merkle_tree.capacity, 8)

    def test_construct(self):
        for i in range(len(elements)):
            # check if the Merkle trees obtained by adding the first i elements,
            # or constructing directing with the first i elements, are identical.
            mt1 = MerkleTree()
            for el in elements[:i]:
                mt1.add(el)
            mt2 = MerkleTree(elements[:i])

            self.assertMerkleTreesEqual(mt1, mt2)

    def test_root_0(self):
        merkle_tree = MerkleTree()
        self.assertEqual(merkle_tree.root, NIL)

    def test_root_1(self):
        merkle_tree = MerkleTree()
        merkle_tree.add(elements[0])
        self.assertEqual(merkle_tree.root, elements[0])

    def test_root_2(self):
        merkle_tree = MerkleTree()
        merkle_tree.add(elements[0])
        merkle_tree.add(elements[1])
        self.assertEqual(merkle_tree.root, H(elements[0] + elements[1]))

    def test_root_3(self):
        merkle_tree = MerkleTree()
        merkle_tree.add(elements[0])
        merkle_tree.add(elements[1])
        merkle_tree.add(elements[2])
        H01 = H(elements[0] + elements[1])
        H2NIL = H(elements[2] + NIL)
        self.assertEqual(merkle_tree.root, H(H01 + H2NIL))

    def test_proof(self):
        merkle_tree = MerkleTree()
        for el in elements:
            merkle_tree.add(el)

        H01 = H(elements[0] + elements[1])
        H45 = H(elements[4] + elements[5])
        H67 = H(NIL + NIL)
        H4567 = H(H45 + H67)

        p = merkle_tree.prove_leaf(3)  # H('of')
        self.assertEqual(p[0], elements[2])  # sibling of leaf 3
        self.assertEqual(p[1], H01)
        self.assertEqual(p[2], H4567)

    def test_prove_verify(self):
        merkle_tree = MerkleTree()
        for el in elements:
            merkle_tree.add(el)

        # for each pair i, j, try if the proof for element i passes when given element j. Should be true iff i == j
        for i in range(len(elements)):
            p = merkle_tree.prove_leaf(i)
            for j in range(len(elements)):
                self.assertEqual(merkle_proof_verify(merkle_tree.root, len(merkle_tree), elements[j], i, p), (i == j))


if __name__ == '__main__':
    unittest.main()
