import unittest
from accumulator.multipointer_loglog import get_representatives, MultipointerLogLogFactory

from .base import BaseAccumulatorTestSuite


class GeneralizedAccumulatorTestSuite(BaseAccumulatorTestSuite, unittest.TestCase):
    """Generalized accumulator test cases."""

    def test_get_representatives(self):
        self.assertEqual(get_representatives(1), [])

        # self.assertEqual(get_representatives(2), [1])
        # self.assertEqual(get_representatives(3), [2])
        # self.assertEqual(get_representatives(4), [3])
        # self.assertEqual(get_representatives(5), [4])
        # self.assertEqual(get_representatives(6), [5, 4])
        # self.assertEqual(get_representatives(7), [6])
        # self.assertEqual(get_representatives(8), [7])
        # self.assertEqual(get_representatives(9), [8])
        # self.assertEqual(get_representatives(10), [9, 8])
        # self.assertEqual(get_representatives(11), [10])
        # self.assertEqual(get_representatives(12), [11, 8])
        # self.assertEqual(get_representatives(13), [12])
        # self.assertEqual(get_representatives(14), [13, 12])
        # self.assertEqual(get_representatives(15), [14])
        # self.assertEqual(get_representatives(16), [15])
        # self.assertEqual(get_representatives(17), [16])
        # self.assertEqual(get_representatives(18), [17, 16])

        # self.assertEqual(get_representatives(1), [])
        # self.assertEqual(get_representatives(32), [31])
        # self.assertEqual(get_representatives(33), [32])
        # self.assertEqual(get_representatives(39), [38, 36])
        # self.assertEqual(get_representatives(40), [39, 32])
        # self.assertEqual(get_representatives(42), [41, 40, 32])

    def get_instances(self):
        factory = MultipointerLogLogFactory()
        return factory.create_accumulator()


if __name__ == '__main__':
    unittest.main()
