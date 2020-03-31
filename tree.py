def hamming_weight(n):
    """Hamming weight of n"""
    result = 0
    while n:
        n &= n - 1
        result += 1

    return result

def bits(n, subtree_width):
    """Returns the bits of n, starting from the least significant bit, using log_2(subtree_width) bits."""
    assert 0 <= n < subtree_width
    result = []
    while subtree_width > 1:
        result.append(n & 1)
        subtree_width //= 2
    return result

def nth_leaf(n):
    """Returns the index of the n-th leaf"""
    return 2*n - hamming_weight(n)

def A001511():
    '''Differences of indices of the leaf nodes. Many interpretations, see https://oeis.org/A001511'''
    yield 1
    for x in A001511():
        yield x+1
        yield 1

def subtree_widths_ascending(k):
    """Returns the number of leafs of each of the complete subtrees, starting from the smallest"""
    result = []
    b = 1
    while k:
        if k & b:
            k -= b
            result.append(b)
        b *= 2
    return result

def subtree_roots_descending(k):
    """Returns the indices of the root nodes of all the subtrees, from the largest (leftmost) to the smallest (rightmost)"""
    result = []
    tree_start = 0
    for cur_tree_width in reversed(subtree_widths_ascending(k)):
        cur_tree_size = 2 * cur_tree_width - 1 # number of nodes of current tree
        result.append(tree_start + cur_tree_size - 1) # index of root
        tree_start += cur_tree_size
    return result


def resize_list(array, new_size, filling=None):
    """Resizes the array to a specified size, truncating or extending with the given filling as needed."""
    size_difference = new_size - len(array)
    if size_difference > 0:
        array.extend([filling for x in range(size_difference)])
    else:
        del array[new_size:]


class SegmentTree:
    """An implicit growable segment-tree"""

    def __init__(self, combine, elements=None):
        self.combine = combine
        if elements is None:
            elements = []

        self.k = len(elements)
        self.nodes = []

        if self.k == 0:
            return

        leaf_index = 0
        while leaf_index < self.k:
            self.nodes.append(elements[leaf_index])

            # for each trailing 1 in the binary rapresentation of leaf_index, we append an internal node (ancestor)
            # we keep track of the size of the subtree rooted at the current node
            t = leaf_index
            shift = 1
            while t % 2 == 1:
                left_sibling_value = self.nodes[len(self.nodes) - 1 - shift]
                parent_node = self.combine(left_sibling_value, self.nodes[-1])
                self.nodes.append(parent_node)
                t = t // 2
                shift = 2*shift + 1

            leaf_index += 1

        resize_list(self.nodes, 2*self.k - 1)
        self.update_temporary_nodes()

    def elements(self):
        """Iterates over all the elements (leafs)."""
        i = 0
        diff = A001511()
        for _ in range(self.k):
            yield self.nodes[i]
            i += next(diff) # pylint: disable=stop-iteration-return

    def update_temporary_nodes(self):
        roots = [r for r in reversed(subtree_roots_descending(self.k))]
        cur_temp_node = roots[0] + 1 # node next to the root of the rightmost subtree
        prev = self.nodes[roots[0]]
        for i in range(len(roots) - 1):
            nxt = self.combine(self.nodes[roots[i+1]], prev)
            self.nodes[cur_temp_node] = nxt
            prev = nxt
            cur_temp_node += 1

    def set_element(self, i, v):
        assert 0 <= i < self.k

        # tracks the number of leaves on the previous trees
        # (that is, the index of the first leaf in the current subtree)
        tree_start = 0

        cur_subtree_width = None
        for cur_subtree_width in reversed(subtree_widths_ascending(self.k)):
            if tree_start + cur_subtree_width > i:
                break
            else:
                # move on to the next tree
                tree_start += cur_subtree_width

        assert cur_subtree_width is not None

        index_in_subtree = i - tree_start # index of the leaf in its subtree
        
        # cur_subtree_width is the number of leaves of the current subtree

        x = nth_leaf(i)
        self.nodes[x] = v # update leaf

        step_size = 2 # if the current node x is a left child (and not the root of the subtree), the parent is x + step_size
        for bit in bits(index_in_subtree, cur_subtree_width):
            # move to the parent; increment by 1 if the current node is a right child, by step_size otherwise
            parent = x + 1 if bit == 1 else x + step_size

            # update current node
            self.nodes[parent] = self.combine(self.nodes[parent - step_size], self.nodes[parent - 1])

            x = parent

            step_size *= 2

        resize_list(self.nodes, 2*self.k - 1)
        # TODO: could optimize slightly by only recomputing the affected temporary nodes
        self.update_temporary_nodes()

    def append_element(self, v):
        self.k += 1
        resize_list(self.nodes, 2*self.k - 1)
        self.set_element(self.k - 1, v)


def main():
    sum_tree = SegmentTree(lambda x, y: x + y, ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    print(sum_tree.nodes)
    print([el for el in sum_tree.elements()])
    for i in ["A", "B", "C", "D", "E", "F"]:
        print(f"Inserting {i}")
        sum_tree.append_element(str(i))
        print(sum_tree.nodes)
        print([el for el in sum_tree.elements()])

if __name__ == "__main__":
    main()
