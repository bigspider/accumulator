import hashlib

NULL_HASH = bytes([0]*32)

# The maximum power of 2 that divides n
def d(n):
    return n & (~(n-1))

# The number of trailing zeros in the binary representation of n
def log_d(n):
    result = 0
    while(n & 1 == 0):
        n = n // 2
        result += 1
    return result

class Accumulator:
    """An accumulator of size 2^logsize"""

    def __init__(self, logsize=20):
        self.i = 0
        self.N = 1 << logsize
        self.D = [NULL_HASH] * (logsize + 1)  # TODO: check if + 1 is needed

    def get_state(self, i):
        return NULL_HASH if i == 0 else self.D[log_d(i)]

    def add(self, x):
        self.i += 1
        i = self.i

        prev_state = self.get_state(i - 1)
        other_state = self.get_state(i - d(i))

        data = x + prev_state + other_state
        result = hashlib.sha256(data).digest()

        self.D[log_d(i)] = result
        return result

# Starting from index i, build a proof for state k
def prove(xs, hashes, i, k):
    assert k <= i

    result = [xs[i], hashes[i - 1], hashes[i - d(i)]]
    if i > k:
        if i - d(i) >= k:
            result += prove(xs, hashes, i - d(i), k)
        else:
            result += prove(xs, hashes, i - 1, k)

    return result

# returns True if `proof` is valid for the statment that the element at position k is x, starting from element i that has S(i) = h
def verify(h, i, k, proof, x):
    assert k <= i
    if len(proof) < 3:
        print("Proof too short")
        return False

    x_i, s_prev, s_pred = proof[0:3]

    # verify that H(x_i|s_prev|s_pred) == h
    if hashlib.sha256(x_i + s_prev + s_pred).digest() != h:
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
    acc = Accumulator(N)
    hashes = [NULL_HASH]
    xs = [NULL_HASH]
    for i in range(1, N + 1):
        x = hashlib.sha256(str(i).encode('utf8')).digest()
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