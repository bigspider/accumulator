from .common import is_power_of_2, pred
from .generalized_accumulator import (
    GeneralizedAccumulatorFactory,
    GeneralizedAccumulator,
    GeneralizedProver,
    GeneralizedVerifier,
)

# Implementation of the generalized accumulator with about log log n "evenly spaced" back-pointers.

# Cost of update: ~2 log log n
# Proof size: O(log n (log log n)^2)


def get_representatives(k: int):
    if k == 1:
        return []

    # if k is even, we also add k - 1
    result = [k - 1] if k % 2 == 0 else []

    t = k
    c = 1
    while pred(t) > 0:
        t = pred(t)
        if is_power_of_2(c):
            result.append(t)
        c += 1
    return result


class MultipointerLogLogFactory(GeneralizedAccumulatorFactory):
    def create_accumulator(self):
        accumulator_manager = GeneralizedAccumulator(get_representatives)
        prover = GeneralizedProver(get_representatives, accumulator_manager)
        verifier = GeneralizedVerifier(get_representatives)
        return accumulator_manager, prover, verifier
