import unittest
from accumulator.common import H
from accumulator.smart_accumulator import SmartAccumulatorFactory, SmartProver

from .base import BaseAccumulatorTestSuite

plain_elements = ["some", "small", "list", "of", "distinct", "elements"]
elements = [H(el) for el in plain_elements]


class SmartAccumulatorTestSuite(BaseAccumulatorTestSuite, unittest.TestCase):
    """Smart accumulator test cases."""

    def get_instances(self):
        factory = SmartAccumulatorFactory()
        return factory.create_accumulator()

    def test_prover_store_roots(self):
        # Test that SmartProver actually stores the accumulators for all the added elements
        acc, prover, _ = self.get_instances()
        roots = dict()
        for i in range(len(elements)):
            acc.add(elements[i])
            roots[i+1] = acc.get_root()  # comparing the roots is enough

        for i in range(1, len(elements) + 1):
            self.assertEqual(prover.R[i], roots[i])

    def test_prover_make_tree_indexes(self):
        self.assertListEqual(SmartProver.make_tree_indexes(4), [3, 2, 4])
        self.assertListEqual(SmartProver.make_tree_indexes(5), [5, 2, 4])
        self.assertListEqual(SmartProver.make_tree_indexes(7), [7, 6, 4])
        self.assertListEqual(SmartProver.make_tree_indexes(8), [7, 6, 4, 8])
        self.assertListEqual(SmartProver.make_tree_indexes(72), [71, 70, 68, 72, 48, 32, 64])

    def test_prover_make_tree(self):
        # Test that SmartProver.make_tree correctly recomputes each Merkle tree of the state
        acc, prover, _ = self.get_instances()
        roots = dict()
        for i in range(len(elements)):
            acc.add(elements[i])
            roots[i+1] = acc.S.root  # comparing the roots is enough

        for i in range(1, len(elements) + 1):
            t = prover.make_tree(i)
            self.assertEqual(t.root, roots[i])


if __name__ == '__main__':
    unittest.main()
