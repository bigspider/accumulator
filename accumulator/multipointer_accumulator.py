from .common import pred, iroot_ceil, floor_lg
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

    l = floor_lg(k)  # k has l + 1 bits
    d = iroot_ceil(p, l)  # d = ceil(floor(log n)^(1/p))

    # computes all the powers of d that are not bigger than l
    exponents = set([1])
    if d > 1:
        t = d
        while t <= l and d > 1:
            exponents.add(t)
            t *= d

    t = pred(k)
    c = 1  # count of how many bits are zeroed
    while t > 0:
        if c in exponents:
            result.append(t)
        t = pred(t)
        c += 1

    return result


class MultipointerAccumulatorFactory(GeneralizedAccumulatorFactory):
    def create_accumulator(self, p: int):
        def get_representatives_p(n: int):
            return get_representatives(n, p)

        accumulator_manager = GeneralizedAccumulator(get_representatives_p)
        prover = GeneralizedProver(get_representatives_p, accumulator_manager)
        verifier = GeneralizedVerifier(get_representatives_p)
        return accumulator_manager, prover, verifier
