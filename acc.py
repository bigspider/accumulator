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
        return NULL_HASH if i == 1 else self.D[log_d(i - 1)]

    def add(self, x):
        self.i += 1
        i = self.i

        prev_state = self.get_state(i - 1)
        j = i - d(i)
        other_state = self.get_state(i - d(i))

        data = x + prev_state + other_state
        result = hashlib.sha256(data).digest()

        self.D[log_d(i)] = result
        return i, result


if __name__ == "__main__":
    acc = Accumulator(20)
    for i in range(20):
        r = acc.add(str(i).encode('utf8'))
        print(r)