from accumulator import H, MerkleTree, merge_hashes, NIL, merkle_proof_verify

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
        assert merkle_tree.root == merge_hashes(elements[0], elements[1])

    def test_root_3(self):
        merkle_tree = MerkleTree()
        merkle_tree.add(elements[0])
        merkle_tree.add(elements[1])
        merkle_tree.add(elements[2])
        H01 = merge_hashes(elements[0], elements[1])
        H2NIL = merge_hashes(elements[2], NIL)
        assert merkle_tree.root == merge_hashes(H01, H2NIL)

    def test_proof(self):
        merkle_tree = MerkleTree()
        for el in elements:
            merkle_tree.add(el)
        
        p = merkle_tree.prove_leaf(3)  # 'of'
        assert p[0] == elements[3]
        # TODO

    def test_prove_verify(self):
        merkle_tree = MerkleTree()
        for el in elements:
            merkle_tree.add(el)
        
        for i in range(len(elements)):
            p = merkle_tree.prove_leaf(i)
            assert merkle_proof_verify(merkle_tree.root, p) == True


if __name__ == '__main__':
    unittest.main()
