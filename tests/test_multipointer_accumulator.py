import unittest
from accumulator.multipointer_accumulator import get_representatives, MultipointerAccumulatorFactory
from accumulator.common import pred

from .base import BaseAccumulatorTestSuite

class GeneralizedAccumulatorTestSuite(BaseAccumulatorTestSuite, unittest.TestCase):
    """Generalized accumulator test cases."""

    def test_get_representatives(self):
        self.assertEqual(get_representatives(1, 1), [])

        self.assertEqual(get_representatives(2, 1), [1])
        self.assertEqual(get_representatives(3, 1), [2])
        self.assertEqual(get_representatives(4, 1), [3])
        self.assertEqual(get_representatives(5, 1), [4])
        self.assertEqual(get_representatives(6, 1), [5, 4])
        self.assertEqual(get_representatives(7, 1), [6])
        self.assertEqual(get_representatives(8, 1), [7])
        self.assertEqual(get_representatives(9, 1), [8])
        self.assertEqual(get_representatives(10, 1), [9, 8])
        self.assertEqual(get_representatives(11, 1), [10])
        self.assertEqual(get_representatives(12, 1), [11, 8])
        self.assertEqual(get_representatives(13, 1), [12])
        self.assertEqual(get_representatives(14, 1), [13, 12])
        self.assertEqual(get_representatives(15, 1), [14])
        self.assertEqual(get_representatives(16, 1), [15])
        self.assertEqual(get_representatives(17, 1), [16])
        self.assertEqual(get_representatives(18, 1), [17, 16])

        self.assertEqual(get_representatives(1, 2), [])
        self.assertEqual(get_representatives(32, 2), [31])
        self.assertEqual(get_representatives(33, 2), [32])
        self.assertEqual(get_representatives(39, 2), [38, 36])
        self.assertEqual(get_representatives(40, 2), [39, 32])
        self.assertEqual(get_representatives(42, 2), [41, 40, 32])


    def get_instances(self):
        factory = MultipointerAccumulatorFactory()
        return factory.create_accumulator(2)


if __name__ == '__main__':
    unittest.main()
