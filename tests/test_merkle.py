from accumulator.common import H, NIL
from accumulator.merkle import get_directions, MerkleTree, merkle_proof_verify

import unittest

plain_elements = ["some", "small", "list", "of", "distinct", "elements"]
elements = [H(el) for el in plain_elements]


class Merkle2TestSuite(unittest.TestCase):
    """Merkle tree implementation test cases."""

    def test_get_directions(self):
        assert get_directions(1, 0) == []
        assert get_directions(2, 0) == [False]
        assert get_directions(2, 1) == [True]

        assert get_directions(3, 0) == [False, False]
        assert get_directions(3, 1) == [False, True]
        assert get_directions(3, 2) == [True]

        assert get_directions(4, 0) == [False, False]
        assert get_directions(4, 1) == [False, True]
        assert get_directions(4, 2) == [True, False]
        assert get_directions(4, 3) == [True, True]

        assert get_directions(5, 0) == [False, False, False]
        assert get_directions(5, 1) == [False, False, True]
        assert get_directions(5, 2) == [False, True, False]
        assert get_directions(5, 3) == [False, True, True]
        assert get_directions(5, 4) == [True]

        assert get_directions(6, 0) == [False, False, False]
        assert get_directions(6, 1) == [False, False, True]
        assert get_directions(6, 2) == [False, True, False]
        assert get_directions(6, 3) == [False, True, True]
        assert get_directions(6, 4) == [True, False]
        assert get_directions(6, 5) == [True, True]

        assert get_directions(7, 0) == [False, False, False]
        assert get_directions(7, 1) == [False, False, True]
        assert get_directions(7, 2) == [False, True, False]
        assert get_directions(7, 3) == [False, True, True]
        assert get_directions(7, 4) == [True, False, False]
        assert get_directions(7, 5) == [True, False, True]
        assert get_directions(7, 6) == [True, True]

        assert get_directions(8, 0) == [False, False, False]
        assert get_directions(8, 1) == [False, False, True]
        assert get_directions(8, 2) == [False, True, False]
        assert get_directions(8, 3) == [False, True, True]
        assert get_directions(8, 4) == [True, False, False]
        assert get_directions(8, 5) == [True, False, True]
        assert get_directions(8, 6) == [True, True, False]
        assert get_directions(8, 7) == [True, True, True]

    def assertMerkleTreesEqual(self, mt1, mt2):
        """Checks that `mt1` and `mt2` are identically equal MerkleTrees"""
        self.assertEqual(len(mt1.leaves), len(mt2.leaves))
        for j in range(len(mt1.leaves)):
            self.assertEqual(mt1.leaves[j].value, mt2.leaves[j].value)

        if mt1.root is None:
            self.assertIsNone(mt2.root)
        else:
            self.assertIsNotNone(mt2.root)
            self.assertEqual(mt1.root, mt2.root)

            self.assertNodeEqual(mt1.root_node, mt2.root_node)

    def assertNodeEqual(self, node1, node2):
        if node1 is None:
            self.assertIsNone(node2)
        else:
            self.assertEqual(node1.value, node2.value)
            if node1.parent is None:
                self.assertIsNone(node2.parent)

            if node1.left is None:
                self.assertIsNone(node2.left)
            else:
                self.assertNodeEqual(node1.left, node2.left)

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

    def test_set_past_last(self):
        # tests that setting the k-th element has exactly the same effect as adding a new element
        mt1 = MerkleTree()
        mt2 = MerkleTree()
        for i in range(len(elements)):
            mt1.add(elements[i])
            mt2.set(len(mt2), elements[i])
            self.assertMerkleTreesEqual(mt1, mt2)

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
        self.assertEqual(merkle_tree.root, H(H01 + elements[2]))

    def test_proof(self):
        merkle_tree = MerkleTree()
        for el in elements:
            merkle_tree.add(el)

        H01 = H(elements[0] + elements[1])
        H45 = H(elements[4] + elements[5])

        p = merkle_tree.prove_leaf(3)  # H('of')
        self.assertEqual(p[0], elements[2])  # sibling of leaf 3
        self.assertEqual(p[1], H01)
        self.assertEqual(p[2], H45)

    def test_prove_verify(self):
        merkle_tree = MerkleTree()
        for el in elements:
            merkle_tree.add(el)

        # for each pair i, j, try if the proof for element i passes when given element j. Should be true iff i == j
        for i in range(len(elements)):
            p = merkle_tree.prove_leaf(i)
            for j in range(len(elements)):
                self.assertEqual(merkle_proof_verify(merkle_tree.root, len(elements), elements[j], i, p), (i == j))


if __name__ == '__main__':
    unittest.main()
