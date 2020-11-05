from .common import pred
from .generalized_accumulator import (
    GeneralizedAccumulatorFactory,
    GeneralizedAccumulator,
    GeneralizedProver,
    GeneralizedVerifier,
)

# Implementation of the generalized accumulator with p "evenly spaced" back-pointers.

# Cost of update: O(p)
# Proof size: O((log n)^(1 + 1/p))


def get_representatives(k: int, p: int):
    if k == 1:
        return []

    # if k is even, we also add k - 1
    result = [k - 1] if k % 2 == 0 else []

    t = k
    for i in range(p):
        t = pred(t)
        if t == 0:
            break
        result.append(t)
    return result


class MultipointerAccumulatorFactory(GeneralizedAccumulatorFactory):
    def create_accumulator(self, p: int):
        def get_representatives_p(n: int):
            return get_representatives(n, p)

        accumulator_manager = GeneralizedAccumulator(get_representatives_p)
        prover = GeneralizedProver(get_representatives_p, accumulator_manager)
        verifier = GeneralizedVerifier(get_representatives_p)
        return accumulator_manager, prover, verifier
