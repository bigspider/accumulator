# Fast additive accumulators

This repo contains presents a work in progress for cryptographic additive accumulator constructions with fast insertion time.
These construction are hash-based, and obtain the following running times:

- First construction: O(1) insertion time and O(log^2 n) proof size 
- Second construction: O(log log n) insertion time and O(log n log log n) proof size

The space occupation for the public state is O(log n) for both constructions.

# Progress

Link to the current writeup [draft]: [Fast hash-based additive accumulators](docs/paper-draft.pdf)

Current progress on the writeup:
- Literature review not fully complete
- Formal definitions and proofs are missing
- Second construction is only a sketch.

Code in this repo:
- [accumulator/accumulator.py](accumulator.py) - simple implementation of the first construction.

