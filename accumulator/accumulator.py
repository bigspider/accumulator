import hashlib
from .event import Event

NULL_HASH = bytes([0] * 32)

# The maximum power of 2 that divides n
def d(n):
    return n & (~(n - 1))


# The number of trailing zeros in the binary representation of n
def log_d(n):
    result = 0
    while n & 1 == 0:
        n = n // 2
        result += 1
    return result

def H(x):
    b = x.encode("utf8") if isinstance(x, str) else x
    return hashlib.sha256(b).digest()

class Accumulator:
    def __init__(self):
        self.k = 0
        self.S = [NULL_HASH]
        self.element_added = Event()

    def __len__(self):
        return self.k

    def increase_counter(self):
        self.k += 1
        if 1 + (1 << (len(self.S) - 1)) <= self.k:
            self.S.append(None)

    def get_state(self, i):
        return NULL_HASH if i == 0 else self.S[log_d(i)]

    def get_root(self):
        return self.get_state(self.k)

    def add(self, x):
        self.increase_counter()

        prev_state = self.get_state(self.k - 1)
        other_state = self.get_state(self.k - d(self.k))

        data = x + prev_state + other_state
        result = H(data)

        self.S[log_d(self.k)] = result

        self.element_added.notify(x, result)
        return result

# TODO: make a "prover" that listens to an accumulator and stores all the elements and hashes, and encapsulates the information to generate proofs
# similarly for a verifier (should it be one class, or two separate classes?)

# Starting from index i, build a proof for state j
def prove(xs, hashes, i, j):
    assert j <= i

    result = [xs[i], hashes[i - 1], hashes[i - d(i)]]
    if i > j:
        if i - d(i) >= j:
            result += prove(xs, hashes, i - d(i), j)
        else:
            result += prove(xs, hashes, i - 1, j)

    return result


# returns True if `proof` is valid for the statment that the element at position k is x, starting from element i that has S(i) = h
def verify(h, i, k, proof, x):
    assert k <= i
    if len(proof) < 3:
        print("Proof too short")
        return False

    x_i, s_prev, s_pred = proof[0:3]

    # verify that H(x_i|s_prev|s_pred) == h
    if H(x_i + s_prev + s_pred) != h:
        print("Hash did not match")
        return False

    if i == k:
        return x_i == x
    else:  # i > k
        if i - d(i) >= k:
            return verify(s_pred, i - d(i), k, proof[3:], x)
        else:
            return verify(s_prev, i - 1, k, proof[3:], x)


def main():
    N = 100
    acc = Accumulator()
    hashes = [NULL_HASH]
    xs = [NULL_HASH]
    for i in range(1, N + 1):
        x = H(str(i))
        xs.append(x)
        r = acc.add(x)
        hashes.append(r)

    proof = prove(xs, hashes, 84, 10)

    verified = verify(hashes[84], 84, 10, proof, xs[10])
    if verified:
        print("Proof passed verification")
    else:
        print("Proof did not pass verification")


if __name__ == "__main__":
    main()
