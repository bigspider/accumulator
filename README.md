# Fast additive accumulators

This repo contains presents a work in progress for cryptographic additive accumulator constructions with fast insertion time.
These construction are hash-based, and obtain the following running performance metrics:

- First construction: O(1) insertion time and O(log^2 n) proof size 
- Second construction: O(log log n) insertion time and O(log n log log n) proof size

The space occupation for the public state is O(log n) for both constructions.

# Progress

Link to the current writeup [draft]: [Fast hash-based additive accumulators](docs/paper-draft.pdf)
Technical presentation (given to the cryptography group at Aarhus University): https://vimeo.com/464504107

Current progress on the writeup:
- Literature review not fully complete
- Formal definitions and proofs are missing

Code in this repo:
- [simple_accumulator.py](accumulator/simple_accumulator.py) - implementation of the first construction.
- [merkle.py](accumulator/merkle.py) - implementation of the flavor of dynamic Merkle trees that is required for the second construction.
- [smart_accumulator.py](accumulator/smart_accumulator.py) - implementation of the full second construction.

The code needs more testing.

The code focuses on simplicity rather than optimizing the constructions to the maximum extent possible. Some known improvements:
- in the simple construction, if *n* is odd, then pred(*n*) = *n* - 1, therefore it is redundant to commit to both R_{*n* - 1} and R_{pred(*n*)} in the definition of R_*n*.
- The Merkle trees are always complete binary trees with 2^*k* leaves when the height is *h* (where unused leaves contain NIL); on average, a constant could be saved in the proof size by not storing the subtrees whose leaves are all NIL. The insertion time is amortized O(log(*n*)) for a tree with *n* leaves, while it is possible to obtain the same in the worst case.
- The SmartProver is not yet very smart; it computes the full Merkle trees on demand rather than saving the necessary precomputed information. Probably not an issue for most applications, though (and it allows to keep the code simpler).
