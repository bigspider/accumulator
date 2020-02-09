def hamming_weight(n):
    """Hamming weight of n"""
    result = 0
    while n:
        n &= n - 1
        result += 1

    return result

def zero_ls1(n):
    """Returns the number obtained by zeroing the least significant 1 of n"""
    return n & (n - 1)

def ls1(n):
    """Returns the number obtained by zeroing every bit of n, except its least significant 1"""
    return n & -n

def nth_leaf(n):
    """Returns the index of the n-th leaf"""
    return 2*n - hamming_weight(n)

def subtree_widths(k):
    """Returns the number of leafs of each of the complete subtrees, starting from the smallest"""
    result = []
    b = 1
    while k:
        if k & b:
            k -= b
            result.append(b)
        b *= 2

def combine(a, b):
    return a + b # TODO: change with the concatenated (sorted) hash


class MerkleTree:
    """A compact growable Merkle tree"""

    def __init__(self, elements=[]):
        self.k = len(elements)
        self.elements = elements

        leaf_index = 0
        nodes = []
        subtree_roots = []
        while leaf_index < self.k:
            nodes.append(elements[leaf_index])

            # for each trailing 1 in the binary rapresentation of leaf_index, we append an internal node (ancestor)
            # we keep track of the size of the subtree rooted at the current node
            t = leaf_index
            shift = 1
            while t % 2 == 1:
                left_sibling = nodes[len(nodes) - 1 - shift]
                parent_node = combine(left_sibling, nodes[-1])
                nodes.append(parent_node)
                t = t // 2
                shift = 2*shift + 1

            leaf_index += 1

        # for each pair of roots of complete subtrees, add a node combining the two roots, starting from the rightmost trees
        if self.k > 0:
            right_child = nodes[-1]
            t = self.k
            p = len(nodes) - 1
            while zero_ls1(t) > 0:
                skip_size = ls1(t) * 2 - 1
                p -= skip_size
                left_child = nodes[p]
                new_node = combine(left_child, right_child)
                nodes.append(new_node)
                right_child = new_node
                t = zero_ls1(t)

        self.nodes = nodes

    def subtree_roots(self):
        pass

    def set_element(self, i, v):
        assert 0 <= i < self.k

        # TODO: don't cheat :P
        new_elements = self.elements[:]
        new_elements[i] = v
        new_tree = MerkleTree(new_elements)

        self.k = new_tree.k
        self.elements = new_tree.elements
        self.nodes = new_tree.nodes

    def append_element(self, v):
        # TODO: don't cheat :P
        new_elements = self.elements[:]
        new_elements.append(v)
        new_tree = MerkleTree(new_elements)

        self.k = new_tree.k
        self.elements = new_tree.elements
        self.nodes = new_tree.nodes


if __name__ == "__main__":
    X = MerkleTree()
    for i in range(12):
        X.append_element(i)
        print(X.nodes)