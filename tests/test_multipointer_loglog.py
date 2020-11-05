import unittest
from accumulator.multipointer_loglog import get_representatives, MultipointerLogLogFactory

from .base import BaseAccumulatorTestSuite


class GeneralizedAccumulatorTestSuite(BaseAccumulatorTestSuite, unittest.TestCase):
    """Generalized accumulator test cases."""

    def test_get_representatives(self):
        self.assertEqual(get_representatives(0b1), [])

        self.assertEqual(get_representatives(0b10), [0b01])
        self.assertEqual(get_representatives(0b11), [0b10])
        self.assertEqual(get_representatives(0b100), [0b11])
        self.assertEqual(get_representatives(0b101), [0b100])
        self.assertEqual(get_representatives(0b110), [0b101, 0b100])
        self.assertEqual(get_representatives(0b111), [0b110, 0b100])
        self.assertEqual(get_representatives(0b1000), [0b0111])
        self.assertEqual(get_representatives(0b1001), [0b1000])
        self.assertEqual(get_representatives(0b1010), [0b1001, 0b1000])
        self.assertEqual(get_representatives(0b1011), [0b1010, 0b1000])
        self.assertEqual(get_representatives(0b1100), [0b1011, 0b1000])
        self.assertEqual(get_representatives(0b1101), [0b1100, 0b1000])
        self.assertEqual(get_representatives(0b1110), [0b1101, 0b1100, 0b1000])
        self.assertEqual(get_representatives(0b1111), [0b1110, 0b1100])
        self.assertEqual(get_representatives(0b10000), [0b01111])
        self.assertEqual(get_representatives(0b10001), [0b10000])
        self.assertEqual(get_representatives(0b10010), [0b10001, 0b10000])
        self.assertEqual(
            get_representatives(0b111001100100101110101001111001110011101010), [
                0b111001100100101110101001111001110011101001,
                0b111001100100101110101001111001110011101000,
                0b111001100100101110101001111001110011100000,
                0b111001100100101110101001111001110010000000,
                0b111001100100101110101001111000000000000000,
                0b111001100100101000000000000000000000000000,
            ])


    def get_instances(self):
        factory = MultipointerLogLogFactory()
        return factory.create_accumulator()


if __name__ == '__main__':
    unittest.main()
