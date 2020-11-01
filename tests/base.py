from typing import Tuple, List
import unittest
from accumulator import H, NIL
from accumulator.factory import AbstractAccumulatorManager, AbstractProver, AbstractVerifier


# pylint: disable=no-member

plain_elements = ["some", "small", "list", "of", "distinct", "elements"]
elements = [H(el) for el in plain_elements]

class BaseAccumulatorTestSuite:
    """Contains the tests that are common for all the accumulators"""

    def get_instances(self) -> Tuple[AbstractAccumulatorManager, AbstractProver, AbstractVerifier]:
        raise NotImplementedError

    def assertAccumulatorEqual(self, acc1, acc2):
        """
        Implementations must have this method, which must verify if two instances of accumulator are structurally
        identical; in other words, the state of the accumulator manager should be deterministic and not depend on its
        history. Tests using this method help verify that.
        """
        raise NotImplementedError

    def test_size(self):
        acc, _, __ = self.get_instances()
        self.assertEqual(len(acc), 0)
        for i in range(len(elements)):
            acc.add(elements[i])
            self.assertEqual(len(acc), i + 1)

    def test_prove_verify_trivial(self):
        # Test with a proof for the latest element
        acc, prover, verifier = self.get_instances()

        for i in range(len(elements)):
            acc.add(elements[i])

        w = prover.prove(len(elements))
        result = verifier.verify(acc.get_root(), len(acc), len(elements), w, elements[-1])
        self.assertTrue(result)

    def test_prove_from_verify_trivial(self):
        # Test with a proof for a past elements, but starting from its own root
        acc, prover, verifier = self.get_instances()

        acc.add(elements[0])
        acc.add(elements[1])
        acc.add(elements[2])
        acc.add(elements[3])
        root_4 = acc.get_root()

        acc.add(elements[4])
        acc.add(elements[5])

        w = prover.prove_from(4, 4)
        result = verifier.verify(root_4, 4, 4, w, elements[4-1])
        self.assertTrue(result)

    def test_prove_verify_all(self):
        acc, prover, verifier = self.get_instances()
        R = [NIL]
        for el in elements:
            acc.add(el)
            R.append(acc.get_root())

        for j in range(1, len(elements) + 1):
            w = prover.prove(j)

            result = verifier.verify(acc.get_root(), len(acc), j, w, elements[j-1])
            self.assertTrue(result)
