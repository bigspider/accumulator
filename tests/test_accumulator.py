from accumulator import Accumulator, H, NULL_HASH, Prover, verify

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_size(self):
        acc = Accumulator()
        acc.add(H("first"))
        acc.add(H("another"))
        acc.add(H("element"))
        assert len(acc) == 3

    def test_proof(self):
        elements = [None, "some", "small", "list", "of", "elements"]
        xs = [None]
        hashes = [NULL_HASH]
        acc = Accumulator()
        prover = Prover(acc)
        for i in range(1, len(elements)):
            x = H(elements[i])
            xs.append(x)
            hashes.append(acc.add(x))

        w = prover.prove(1)

        assert verify(acc.get_root(), len(acc), 1, w, xs[1])

if __name__ == '__main__':
    unittest.main()
