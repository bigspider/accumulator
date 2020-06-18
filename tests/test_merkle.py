from accumulator import H, MerkleTree, NIL, merkle_proof_verify

import unittest

plain_elements = ["some", "small", "list", "of", "distinct", "elements"]
elements = [H(el) for el in plain_elements]


class MerkleTestSuite(unittest.TestCase):
    """Merkle tree implementation test cases."""

    def test_add_1(self):
        merkle_tree = MerkleTree()
        assert(len(merkle_tree) == 0)
        merkle_tree.add(elements[0])
        assert len(merkle_tree) == 1
        assert merkle_tree.get(0) == elements[0]

    def test_add_2(self):
        merkle_tree = MerkleTree()
        merkle_tree.add(elements[0])
        merkle_tree.add(elements[1])
        assert len(merkle_tree) == 2
        assert merkle_tree.get(0) == elements[0]
        assert merkle_tree.get(1) == elements[1]

    def test_capacity(self):
        merkle_tree = MerkleTree()
        assert merkle_tree.capacity == 1
        merkle_tree.add(elements[0])
        assert merkle_tree.capacity == 1
        merkle_tree.add(elements[1])
        assert merkle_tree.capacity == 2
        merkle_tree.add(elements[2])
        assert merkle_tree.capacity == 4
        merkle_tree.add(elements[3])
        assert merkle_tree.capacity == 4
        merkle_tree.add(elements[4])
        assert merkle_tree.capacity == 8
        merkle_tree.add(elements[5])
        assert merkle_tree.capacity == 8


    def test_add_many(self):
        merkle_tree = MerkleTree()
        for i in range(len(elements)):
            merkle_tree.add(elements[i])
            assert len(merkle_tree) == i + 1
            assert merkle_tree.get(i) == elements[i]

    def test_root_0(self):
        merkle_tree = MerkleTree()
        assert merkle_tree.root == NIL

    def test_root_1(self):
        merkle_tree = MerkleTree()
        merkle_tree.add(elements[0])
        assert merkle_tree.root == elements[0]

    def test_root_2(self):
        merkle_tree = MerkleTree()
        merkle_tree.add(elements[0])
        merkle_tree.add(elements[1])
        assert merkle_tree.root == H(elements[0] + elements[1])

    def test_root_3(self):
        merkle_tree = MerkleTree()
        merkle_tree.add(elements[0])
        merkle_tree.add(elements[1])
        merkle_tree.add(elements[2])
        H01 = H(elements[0] + elements[1])
        H2NIL = H(elements[2] + NIL)
        assert merkle_tree.root == H(H01 + H2NIL)

    def test_proof(self):
        merkle_tree = MerkleTree()
        for el in elements:
            merkle_tree.add(el)

        H01 = H(elements[0] + elements[1])
        H45 = H(elements[4] + elements[5])
        H67 = H(NIL + NIL)
        H4567 = H(H45 + H67)

        p = merkle_tree.prove_leaf(3)  # H('of')
        assert p[0] == elements[2] # sibling of leaf 3
        assert p[1] == H01
        assert p[2] == H4567

    def test_prove_verify(self):
        merkle_tree = MerkleTree()
        for el in elements:
            merkle_tree.add(el)

        # for each pair i, j, try if the proof for element i passes when given element j. Should be true iff i == j
        for i in range(len(elements)):
            p = merkle_tree.prove_leaf(i)
            for j in range(len(elements)):
                assert merkle_proof_verify(merkle_tree.root, elements[j], i, p) == (i == j)


if __name__ == '__main__':
    unittest.main()
