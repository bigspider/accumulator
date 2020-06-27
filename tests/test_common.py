from accumulator import hook_index, floor_lg, ceil_lg

import unittest

class CommonTestSuite(unittest.TestCase):
    """Tests for functions in common."""

    def test_hook_index(self):
        assert hook_index(0b11000101010100101001000, 0) == 0b11000101010100101000111
        assert hook_index(0b11000101010100101001000, 1) == 0b11000101010100101000110
        assert hook_index(0b11000101010100101001000, 2) == 0b11000101010100101000100
        assert hook_index(0b11000101010100101001000, 3) == 0b11000101010100101001000
        assert hook_index(0b11000101010100101001000, 4) == 0b11000101010100100110000
        assert hook_index(0b11000101010100101001000, 5) == 0b11000101010100100100000
        assert hook_index(0b11000101010100101001000, 6) == 0b11000101010100101000000
        assert hook_index(0b11000101010100101001000, 7) == 0b11000101010100010000000

    def test_floor_lg(self):
        assert(floor_lg(1) == 0)
        assert(floor_lg(2) == 1)
        assert(floor_lg(3) == 1)
        assert(floor_lg(4) == 2)
        assert(floor_lg(5) == 2)
        assert(floor_lg(6) == 2)
        assert(floor_lg(7) == 2)
        assert(floor_lg(8) == 3)
        assert(floor_lg(9) == 3)
        assert(floor_lg(10) == 3)
        assert(floor_lg(11) == 3)
        assert(floor_lg(12) == 3)
        assert(floor_lg(13) == 3)
        assert(floor_lg(14) == 3)
        assert(floor_lg(15) == 3)
        assert(floor_lg(16) == 4)
        assert(floor_lg(17) == 4)

    def test_ceil_lg(self):
        assert(ceil_lg(1) == 0)
        assert(ceil_lg(2) == 1)
        assert(ceil_lg(3) == 2)
        assert(ceil_lg(4) == 2)
        assert(ceil_lg(5) == 3)
        assert(ceil_lg(6) == 3)
        assert(ceil_lg(7) == 3)
        assert(ceil_lg(8) == 3)
        assert(ceil_lg(9) == 4)
        assert(ceil_lg(10) == 4)
        assert(ceil_lg(11) == 4)
        assert(ceil_lg(12) == 4)
        assert(ceil_lg(13) == 4)
        assert(ceil_lg(14) == 4)
        assert(ceil_lg(15) == 4)
        assert(ceil_lg(16) == 4)
        assert(ceil_lg(17) == 5)


if __name__ == '__main__':
    unittest.main()
