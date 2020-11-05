import unittest
from accumulator.simple_accumulator import SimpleAccumulatorFactory

from .base import BaseAccumulatorTestSuite


class SimpleAccumulatorTestSuite(BaseAccumulatorTestSuite, unittest.TestCase):
    """Simple accumulator test cases."""

    def get_instances(self):
        factory = SimpleAccumulatorFactory()
        return factory.create_accumulator()


if __name__ == '__main__':
    unittest.main()
