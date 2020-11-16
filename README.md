# Fast additive accumulators

This repo contains a work in progress for cryptographic additive accumulator constructions with fast insertion time.
These construction are hash-based, and obtain the following running performance metrics:

- First main construction: O(1) insertion time and O(log^2 n) proof size 
- Second main construction: O(log log n) insertion time and O(log n log log n) proof size

The space occupation for the public state is O(log n) for both constructions.

Some other recent developments are sketched below.

Link to the current writeup [draft]: [Fast hash-based additive accumulators](docs/paper-draft.pdf)

Technical presentation (given to the cryptography group at Aarhus University): https://vimeo.com/464504107

# Progress

Current progress on the writeup:
- Literature review not fully complete
- Formal definitions and proofs are missing

Code in this repo:
- [simple_accumulator.py](accumulator/simple_accumulator.py) - implementation of the first construction.
- [merkle.py](accumulator/merkle.py) - implementation of the flavor of dynamic Merkle trees that is required for the second construction.
- [smart_accumulator.py](accumulator/smart_accumulator.py) - implementation of the full second construction.

Not yet described in the paper draft:
- [multipointer_accumulator.py](accumulator/multipointer_accumulator.py) - a generalization of the first construction. For any fixed integer p >= 1, it achieves insertion cost O_p(1) and proof size O_p((log n) ^ (1 + 1/p)). With p = 1, it reduces to the simple_accumulator.
- [multipointer_loglog.py](accumulator/multipointer_loglog.py) - a modification of the multipointer accumulator using a non-constant p; achieves insertion cost O(log log n) and proof size O(log n log log n log log log n) (true story)

Open problem:
- It might be possible to modify the multipointer_loglog construction to have strictly better insertion cost than log log n (while still not constant). That would give an interesting solution in between the simple_accumulator and the smart_accumulator!

The code needs more testing.

The code focuses on simplicity rather than optimizing the constructions to the maximum extent possible. Some known improvements:
- in the simple construction, if *n* is odd, then pred(*n*) = *n* - 1, therefore it is redundant to commit to both R_{*n* - 1} and R_{pred(*n*)} in the definition of R_*n*.
- The SmartProver is not yet very smart; it computes the full Merkle trees on demand rather than saving the necessary precomputed information. Probably not an issue for most applications, though (and it allows to keep the code simpler).
