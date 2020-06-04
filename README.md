# Fast additive accumulators

These report presents a work in progress for cryptographic additive accumulator constructions with fast insertion time.
These construction are hash-based, and obtain the following running times:

- First construction: O(1) insertion time and O(log^2 n) proof size 
- Second construction: O(log log n) insertion time and O(log n log log n) proof size

# Progress

Link to the current writeup: TODO

Current progress on the writeup:
- Literature review not fully complete
- Formal definitions and proofs are missing
- First construction is fully defined
- Second construction is sketched

Code in this repo:
- ´accumulator.py´ is a toy implementation of the first (simpler) construction.
- ´tree.py´: experimental data structure for representing segment trees