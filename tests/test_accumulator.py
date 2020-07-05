from accumulator import Accumulator, H, NIL, Prover, verify

import unittest

plain_elements = ["some", "small", "list", "of", "distinct", "elements"]
elements = [H(el) for el in plain_elements]


class AccumulatorTestSuite(unittest.TestCase):
    """Simple accumulator test cases."""

    def test_size(self):
        acc = Accumulator()
        self.assertEqual(len(acc), 0)
        for i in range(len(elements)):
            acc.add(elements[i])
            self.assertEqual(len(acc), i + 1)

    def test_prove_verify_all(self):
        acc = Accumulator()
        prover = Prover(acc)
        R = [NIL]
        for el in elements:
            acc.add(el)
            R.append(acc.get_root())

        for j in range(1, len(elements) + 1):
            w = prover.prove(j)

            result = verify(acc.get_root(), len(acc), j, w, elements[j-1])
            self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
