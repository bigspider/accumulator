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
        self.D = [NULL_HASH] * (logsize + 1)  # check if + 1 is needed

    def get_state(self, i):
        return NULL_HASH if i == 0 else self.D[log_d(i)]

    def add(self, x):
        self.i += 1
        i = self.i

        prev_state = self.get_state(i - 1)
        j = i - d(i)
        other_state = self.get_state(i - d(i))

        data = x + prev_state + other_state
        result = hashlib.sha256(data).digest()

        self.D[log_d(i)] = result
        return result

# Starting from index i, build a proof for state k
def prove(xs, hashes, i, k):
    print('{0:07b}'.format(i))
    assert k <= i

    result = [xs[i], hashes[i - 1], hashes[i - d(i)]]
    if i > k:
        if i - d(i) >= k:
            result += prove(xs, hashes, i - d(i), k)
        else:
            result += prove(xs, hashes, i - 1, k)


    return result

# returns True if `proof` is valid for the statment that the element at position k is x, starting from element i
def verify(i, k, proof, x):
    pass

def main():
    N = 100
    acc = Accumulator(N)
    hashes = [NULL_HASH]
    xs = [NULL_HASH]
    for i in range(1, N + 1):
        x = str(i).encode('utf8')
        xs.append(x)
        r = acc.add(x)
        hashes.append(r)
    print(hashes)


    proof = prove(xs, hashes, 84, 10)

if __name__ == "__main__":
    main()