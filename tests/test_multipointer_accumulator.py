import unittest
from accumulator.multipointer_accumulator import get_representatives, MultipointerAccumulatorFactory

from .base import BaseAccumulatorTestSuite


class GeneralizedAccumulatorTestSuite(BaseAccumulatorTestSuite, unittest.TestCase):
    """Generalized accumulator test cases."""

    def test_get_representatives(self):
        # floor(log n) = 9
        # ceil(floor(log n)^(1/2)) = 3
        self.assertEqual(get_representatives(0b1000000001, 2), [0b1000000000])
        self.assertEqual(get_representatives(0b1000111001, 2), [0b1000111000, 0b1000100000])
        self.assertEqual(get_representatives(0b1110111110, 2), [0b1110111101, 0b1110111100, 0b1110110000])
        self.assertEqual(get_representatives(0b1110111111, 2), [0b1110111110, 0b1110111000])
        self.assertEqual(get_representatives(0b1111111111, 2), [0b1111111110, 0b1111111000, 0b1000000000])

        # 2^10 <= n < 2^11
        # floor(log n) = 10
        # ceil(floor(log n)^(1/2)) = 4
        self.assertEqual(get_representatives(0b10000000001, 2), [0b10000000000])
        self.assertEqual(get_representatives(0b10011011010, 2), [0b10011011001, 0b10011011000, 0b10010000000])
        self.assertEqual(get_representatives(0b11111111111, 2), [0b11111111110, 0b11111110000])

        # 2^15 <= n < 2^16
        # floor(log n) = 15
        # ceil(floor(log n)^(1/2)) = 4
        self.assertEqual(get_representatives(0b1000000000000000, 2), [0b0111111111111111])
        self.assertEqual(get_representatives(0b1000000000000001, 2), [0b1000000000000000])
        self.assertEqual(get_representatives(0b1111111111111111, 2), [0b1111111111111110, 0b1111111111110000])

        # 2^16 <= n < 2^17
        # floor(log n) = 16
        # ceil(floor(log n)^(1/2)) = 4
        self.assertEqual(get_representatives(0b10000000000000001, 2), [0b10000000000000000])
        self.assertEqual(
            get_representatives(0b11111111111111111, 2),
            [0b11111111111111110, 0b11111111111110000, 0b10000000000000000]
        )

        # 2^8 <= n < 2^9
        # floor(log n) = 8
        # ceil(floor(log n)^(1/3)) = 2
        self.assertEqual(get_representatives(0b100000000, 3), [0b011111111])
        self.assertEqual(get_representatives(0b111111111, 3), [0b111111110, 0b111111100, 0b111110000, 0b100000000])

    def get_instances(self):
        factory = MultipointerAccumulatorFactory()
        return factory.create_accumulator(2)


if __name__ == '__main__':
    unittest.main()
